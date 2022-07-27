using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Community.Models;
using RabbitMQ.Client;
using ContainerManagement;
using Newtonsoft.Json;
using System.Text;
using static ResponseUtils.ResponseUtils;
using System.Net.Http;
using ContainerCenter;
using Grpc.Net.Client;
using System.Text.Json;
using System.IO;
using Community.Dto;

namespace Community.Controllers
{
    [Route("api/[controller]/[action]")]
    [ApiController]
    public class ContainersController : ControllerBase
    {
        private readonly MyDbContext _context;
        private IConnection connection;
        private IModel channel;
        private IHttpClientFactory _factory;
        private ContainerService.ContainerServiceClient gRpcClient;

        public ContainersController(MyDbContext context, IHttpClientFactory factory)
        {
            _context = context;
            var connectionFactory = new ConnectionFactory()
            {
                HostName = MyConfig.MqHostName,
                UserName = MyConfig.MqUsername,
                Password = MyConfig.MqPassword
            };
            connection = connectionFactory.CreateConnection();
            channel = connection.CreateModel();
            channel.BasicQos(0, 1, false);
            _factory = factory;
            var gRpcChannel = GrpcChannel.ForAddress("https://localhost:12000");
            gRpcClient = new ContainerService.ContainerServiceClient(gRpcChannel);
        }

        // GET: api/Containers/GetContainer/5
        [HttpGet("{username}")]
        public ActionResult<StandardResponse> GetContainer(string username)
        {
            var containerList = _context.Container.Where(c => c.Username == username).ToList();
            return NewResponse(200, "success", containerList);
        }

        // POST: api/Containers/PostContainer
        [HttpPost]
        public async Task<ActionResult<StandardResponse>> PostContainer(Container container)
        {
            _context.Container.Add(container);
            container.CreateTime = DateTime.Now;
            await _context.SaveChangesAsync();
            string message = JsonConvert.SerializeObject(container);
            var body = Encoding.UTF8.GetBytes(message);
            channel.BasicPublish("", "mlab", null, body);
            return NewResponse(200, "success", container);
        }

        // POST: api/Containers/DeleteContainer/5
        [HttpPost("{id}")]
        public async Task<ActionResult<StandardResponse>> DeleteContainer(int id)
        {
            var container = await _context.Container.FindAsync(id);
            if (container == null)
            {
                return NotFound();
            }
            _context.Container.Remove(container);
            await _context.SaveChangesAsync();
            await StopContainer(id);
            return NewResponse(200, "删除成功", null);
        }

        // POST: api/Containers/StartContainer
        [HttpPost("{id}")]
        public async Task<ActionResult<StandardResponse>> StartContainer(int id)
        {
            string ipAddress = gRpcClient.getServerIp(new ServerRequest()
            {
                ContainerId = id.ToString()
            }).Ip;
            if (ipAddress.Length == 0)
            {
                System.Diagnostics.Debug.WriteLine("not found");
                return NotFound();
            }
            var container = await _context.Container.FindAsync(id);
            if (container == null)
            {
                System.Diagnostics.Debug.WriteLine("not found");
                return NotFound();
            }
            var containerJSON = new StringContent(
                System.Text.Json.JsonSerializer.Serialize(container, new JsonSerializerOptions()),
                Encoding.UTF8,
                "application/json");
            using var httpResponse = await _factory.CreateClient()
                .PostAsync("http://" + ipAddress + ":13000/api/docker/Start", containerJSON);
            if (httpResponse.IsSuccessStatusCode)
            {
                String body = await httpResponse.Content.ReadAsStringAsync();
                return await ConnectContainer(id);
            }
            else
            {
                return NewResponse(200, "fail", null);
            }
        }

        [HttpGet]
        public async Task<ActionResult<StandardResponse>> ConnectContainer(int id)
        {
            string ipAddress = gRpcClient.getServerIp(new ServerRequest()
            {
                ContainerId = id.ToString()
            }).Ip;
            if (ipAddress.Length == 0)
            {
                return NotFound();
            }
            var container = await _context.Container.FindAsync(id);
            if (container == null)
            {
                System.Diagnostics.Debug.WriteLine("not found");
                return NotFound();
            }
            var request = new HttpRequestMessage(HttpMethod.Get,
                "http://"+ipAddress+":13000/api/docker/Connect/"+id);
            var client = _factory.CreateClient();
            var response = await client.SendAsync(request);
            if (response.IsSuccessStatusCode)
            {
                String body = await response.Content.ReadAsStringAsync();
                return NewResponse(200, "success", body);       
            } else
            {
                return NewResponse(200, "fail", null);
            }
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<StandardResponse>> StopContainer(int id)
        {
            string ipAddress = gRpcClient.getServerIp(new ServerRequest()
            {
                ContainerId = id.ToString()
            }).Ip;
            if (ipAddress.Length == 0)
            {
                return NotFound();
            }
            var container = await _context.Container.FindAsync(id);
            if (container == null)
            {
                return NotFound();
            }
            var request = new HttpRequestMessage(HttpMethod.Get,
                "http://" + ipAddress + ":13000/api/docker/Stop/" + id);
            var client = _factory.CreateClient();
            var response = await client.SendAsync(request);
            if (response.IsSuccessStatusCode)
            {
                return NewResponse(200, "关闭成功", null);
            }
            else
            {
                return NewResponse(200, "关闭失败", null);
            }
        }

        [HttpPost]
        public async Task<ActionResult<StandardResponse>> CopyContainer(Post post)
        {
            // Assume the username of post is the user who want to copy the container
            // NOT THE AURTHOR
            string ipAddress = gRpcClient.getServerIp(new ServerRequest()
            {
                ContainerId = post.ContainerId.ToString()
            }).Ip;
            if (ipAddress.Length == 0)
            {
                return NotFound();
            }
            Container container = await _context.Container.FindAsync(post.ContainerId);
            Container newContainer = new Container()
            {
                Username = post.Username,
                ContainerName = container.ContainerName,
                CreateTime = DateTime.Now,
                Type = container.Type
            };
            await _context.AddAsync(newContainer);
            await _context.SaveChangesAsync();
            CopyContainerDto dto = new CopyContainerDto()
            {
                ContainerId = newContainer.ContainerId,
                ImageId = post.PostId
            };
            var dtoJSON = new StringContent(
                System.Text.Json.JsonSerializer.Serialize(dto, new JsonSerializerOptions()),
                Encoding.UTF8,
                "application/json");
            using var httpResponse = await _factory.CreateClient()
                .PostAsync("http://" + ipAddress + ":13000/api/docker/Import", dtoJSON);
            if (httpResponse.IsSuccessStatusCode)
            {
                return NewResponse(200, "复制成功", null);
            }
            else
            {
                return NewResponse(200, "复制失败", null);
            }
        }
        private bool ContainerExists(int id)
        {
            return _context.Container.Any(e => e.ContainerId == id);
        }
    }
}
