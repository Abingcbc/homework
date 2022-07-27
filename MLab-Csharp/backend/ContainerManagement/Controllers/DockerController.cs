using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net.WebSockets;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using COMLibLib;
using ContainerManagement.Dto;
using ContainerManagement.Models;
using ContainerManagement.Utils;
using CSRedis;
using Docker.DotNet;
using Docker.DotNet.Models;
using FluentScheduler;
using LogManagement;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using static ContainerManagement.Utils.ResponseUtils;

namespace ContainerManagement.Controllers
{
    [Route("api/[controller]/[action]")]
    [ApiController]
    public class DockerController : ControllerBase
    {
        private readonly MyDbContext _context;
        private DockerClient client;
        private CSRedisClient cSRedisClient;
        private CSRedisClient cSRedisClient2;

        public DockerController(MyDbContext context)
        {
            _context = context;
            client = new DockerClientConfiguration(new Uri("http://localhost:2375")).CreateClient();
            cSRedisClient = new CSRedisClient("127.0.0.1:6379,defaultDatabase=11");
            RedisHelper.Initialization(cSRedisClient);
            cSRedisClient2 = new CSRedisClient("127.0.0.1:6379,defaultDatabase=10");
            RedisHelper.Initialization(cSRedisClient2);
        }

        [HttpPost]
        public async Task<ActionResult<String>> Start(Container container)
        {
            string startString = "mlab" + container.ContainerId;
            var containerList = await client.Containers.ListContainersAsync(new ContainersListParameters()
            {
                All = false
            });
            foreach (var con in containerList)
            {
                if (con.Names[0] == startString)
                {
                    return await Connect(container.ContainerId);
                }
            }
            await Task.Run(() =>
            {
                client.Containers.StartContainerAsync(startString, new ContainerStartParameters()
                {

                }).GetAwaiter().GetResult();
            });
            Debug.WriteLine("start monitor");
            // 开启监控
            var registry = new Registry();
            string logsFilePath = startString + ".txt";
            // 创建对 CPU 占用百分比的性能计数器。
            var cpuCounter = new PerformanceCounter("Processor", "% Processor Time", "_Total");
            // 创建内存占用字节数的性能计数器
            var ramCounter = new PerformanceCounter("Memory", "Available MBytes");
            // 覆盖原来的log
            try
            {
                StreamWriter outputFile = new StreamWriter(logsFilePath);
                //outputFile.WriteLine(BindingClass.getMemoryInfo());
                float cpuUsage = cpuCounter.NextValue();
                float ramUsage = ramCounter.NextValue();
                //LogWriter logWriter = new LogWriter();
                outputFile.WriteLine("[" + DateTime.Now + "] CPU: " + cpuUsage + "% Memory Usage: " + ramUsage + "MB");
                outputFile.Close();
                outputFile.Dispose();
                Debug.WriteLine("one monitor");
                registry.Schedule(() =>
                {
                    try
                    {
                        Debug.WriteLine("schedule monitor");
                        StreamWriter outputFile2 = new StreamWriter(logsFilePath, true);
                        //outputFile.WriteLine(BindingClass.getMemoryInfo());
                        float cpuUsage = cpuCounter.NextValue();
                        float ramUsage = ramCounter.NextValue();
                        //LogWriter logWriter = new LogWriter();
                        outputFile2.WriteLine("[" + DateTime.Now + "] CPU: " + cpuUsage + "% Memory Usage: " + ramUsage + "MB");
                        outputFile2.Close();
                        outputFile2.Dispose();
                    }
                    catch (Exception)
                    {
                        Debug.WriteLine("monitor error");
                    }
                }).ToRunEvery(5).Seconds();
                JobManager.Initialize(registry);
            }
            catch (Exception)
            {

            }
            return await Connect(container.ContainerId);
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<String>> Connect(int id)
        {
            System.Diagnostics.Debug.WriteLine("connect to " + id);
            string name = "mlab" + id;
            Stream stream = await client.Containers.GetContainerLogsAsync(name,
                new ContainerLogsParameters()
                {
                    ShowStdout = true,
                    ShowStderr = true
                });
            if (stream == null)
            {
                return NotFound();
            }
            StreamReader reader = new StreamReader(stream, new UTF8Encoding(false));
            string logs = await reader.ReadToEndAsync();
            System.Diagnostics.Debug.WriteLine(logs);
            int start = logs.IndexOf("http://127.0.0.1");
            if (start < 0)
            {
                return NotFound();
            }
            string left = logs.Substring(start);
            int end = left.IndexOf("\n");
            string result = left.Substring(0, end);
            string hostPort = cSRedisClient.Get(id.ToString());
            result = result.Replace("8888", hostPort);

            return result;
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<StandardResponse>> Stop(int id)
        {
            string name = "mlab" + id;
            await client.Containers.StopContainerAsync(name, new ContainerStopParameters()
            {
                WaitBeforeKillSeconds = 10
            });
            JobManager.Stop();
            return NewResponse(200, "关闭成功", null);
        }

        [HttpPost]
        public async Task<ActionResult<String>> Export(Post post)
        {
            string name = "mlab" + post.ContainerId;
            CommitContainerChangesResponse reponse = await client.Images.CommitContainerChangesAsync(new CommitContainerChangesParameters()
            {
                ContainerID = name,
                RepositoryName = post.PostId.ToString()
            });
            return reponse.ID;
        }

        [HttpPost]
        public async Task<ActionResult<StandardResponse>> Import(CopyContainerDto dto)
        {
            string startString = "mlab" + dto.ContainerId;
            var imageList = await client.Images.ListImagesAsync(new ImagesListParameters());
            string imageId = "";
            foreach (var image in imageList)
            {
                if (image.RepoTags[0].StartsWith(dto.ImageId.ToString()))
                {
                    imageId = image.ID;
                    break;
                }
            }
            if (imageId == "")
            {
                return NotFound();
            }
            string mHostPort = (20000 + dto.ContainerId).ToString();
            var result = await client.Containers.CreateContainerAsync(new Docker.DotNet.Models.CreateContainerParameters()
            {
                Image = imageId,
                Name = "mlab" + dto.ContainerId.ToString(),
                ExposedPorts = new Dictionary<string, EmptyStruct>()
                    {
                        {"8888",new EmptyStruct()}
                    },
                HostConfig = new HostConfig
                {
                    PortBindings = new Dictionary<string, IList<PortBinding>> {
                            {
                                "8888", new List<PortBinding> {
                                    new PortBinding {
                                        HostPort = mHostPort
                                    }
                                }
                            }
                        }
                }
            });
            await cSRedisClient2.SetAsync(dto.ContainerId.ToString(), "127.0.0.1");
            await cSRedisClient.SetAsync(dto.ContainerId.ToString(), mHostPort);
            return NewResponse(200, "success", null);
        }

        [HttpGet("{id}")]
        public FileStreamResult Download(int id)
        {
            string name = "mlab" + id;
            return File(System.IO.File.OpenRead(name+".txt"), "application/octet-stream", name+".txt");
        }
    }
}
