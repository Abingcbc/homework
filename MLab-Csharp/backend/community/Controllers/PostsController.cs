using System;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Community.Models;
using Grpc.Net.Client;
using ContainerCenter;
using static ResponseUtils.ResponseUtils;
using System.Net.Http;
using System.Text.Json;
using System.Text;
using System.Collections;
using System.Collections.Generic;

namespace Community.Controllers
{
    [Route("api")]
    [ApiController]
    public class PostsController : ControllerBase
    {
        private readonly MyDbContext _context;
        private IHttpClientFactory _factory;
        private ContainerService.ContainerServiceClient gRpcClient;

        public PostsController(MyDbContext context, IHttpClientFactory factory)
        {
            _context = context;
            _factory = factory;
            var gRpcChannel = GrpcChannel.ForAddress("https://localhost:12000");
            gRpcClient = new ContainerService.ContainerServiceClient(gRpcChannel);
        }

        [Route("GetPost")]
        [HttpGet]
        public async Task<ActionResult<StandardResponse>> GetPost()
        {
            var postList = await _context.Post.ToListAsync();
            foreach (var post in postList)
            {
                if (post.ContainerId != 0)
                {
                    post.Container = await _context.Container.FindAsync(post.ContainerId);
                }
            }
            return NewResponse(200, "success", postList);
        }
        
        [Route("GetMyPost")]
        [HttpGet]
        public async Task<ActionResult<StandardResponse>> GetMyPost(string username)
        {
            var postList = _context.Post.Where(p => p.Username == username).ToList();
            foreach (var post in postList)
            {
                if (post.ContainerId != 0)
                {
                    post.Container = await _context.Container.FindAsync(post.ContainerId);
                }
            }
            return NewResponse(200, "success", postList);
        }

        [Route("GetLikePost")]
        [HttpGet]
        public async Task<ActionResult<StandardResponse>> GetLikePost(string username)
        {
            var likeList = _context.Likes.Where(l => l.Username == username).ToList();
            List<Post> postList = new List<Post>();
            foreach (var like in likeList)
            {
                postList.Add(_context.Post.Find(like.PostId));
            }
            foreach (var post in postList)
            {
                if (post.ContainerId != 0)
                {
                    post.Container = await _context.Container.FindAsync(post.ContainerId);
                }
            }
            return NewResponse(200, "success", postList);
        }

        [Route("SearchPost")]
        [HttpGet]
        public async Task<ActionResult<StandardResponse>> SearchPost(string keyword)
        {
            var postList = await _context.Post.Where(p => p.Title.Contains(keyword)
            || p.Content.Contains(keyword)).ToListAsync();
            foreach (var post in postList)
            {
                if (post.ContainerId != 0)
                {
                    post.Container = await _context.Container.FindAsync(post.ContainerId);
                }
            }
            return NewResponse(200, "success", postList);
        }

        [Route("GetPostDetail")]
        [HttpGet]
        public async Task<ActionResult<StandardResponse>> GetPostDetail(int id)
        {
            System.Diagnostics.Debug.WriteLine("------- " + id + " -------");
            var post = await _context.Post.Include(p => p.Container)
                .Include(p => p.UsernameNavigation)
                .Include(p => p.Comment)
                .Include(p => p.Likes)
                .Where(p => p.PostId == id).ToListAsync();

            if (post == null)
            {
                return NotFound();
            }

            return NewResponse(200, "success", post[0]);
        }

        [Route("PostPost")]
        [HttpPost]
        public async Task<ActionResult<StandardResponse>> PostPost(Post post)
        {
            post.CreateTime = DateTime.Now;
            post.LikeNum = 0;
            post.CommentNum = 0;
            post.Status = 0;
            _context.Post.Add(post);
            await _context.SaveChangesAsync();
            if (post.ContainerId != 0)
            {
                string ipAddress = gRpcClient.getServerIp(new ServerRequest()
                {
                    ContainerId = post.ContainerId.ToString()
                }).Ip;
                if (ipAddress.Length == 0)
                {
                    return NotFound();
                }
                var containerJSON = new StringContent(
                    JsonSerializer.Serialize(post, new JsonSerializerOptions()),
                    Encoding.UTF8,
                    "application/json");
                using var httpResponse = await _factory.CreateClient()
                    .PostAsync("http://" + ipAddress + ":13000/api/docker/Export", containerJSON);
                if (!httpResponse.IsSuccessStatusCode)
                {
                    System.Diagnostics.Debug.WriteLine(httpResponse);
                    return NewResponse(200, "fail", null);
                }
            }
            return NewResponse(200, "success", post);
        }

        [Route("DeletePost")]
        [HttpPost("{id}")]
        public async Task<ActionResult<StandardResponse>> DeletePost(int id)
        {
            var post = await _context.Post.FindAsync(id);
            if (post == null)
            {
                return NotFound();
            }

            _context.Post.Remove(post);
            await _context.SaveChangesAsync();

            return NewResponse(200, "success", null);
        }

        


        private bool PostExists(int id)
        {
            return _context.Post.Any(e => e.PostId == id);
        }
    }
}
