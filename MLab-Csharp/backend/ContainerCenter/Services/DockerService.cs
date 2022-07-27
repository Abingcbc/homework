using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using CSRedis;
using Docker.DotNet;
using Docker.DotNet.Models;
using Grpc.Core;
using Microsoft.Extensions.Logging;

namespace ContainerCenter
{
    public class DockerService : ContainerService.ContainerServiceBase
    {
        private readonly ILogger<DockerService> _logger;
        private CSRedisClient cSRedisClient;
        public DockerService(ILogger<DockerService> logger)
        {
            _logger = logger;
            cSRedisClient = new CSRedisClient("127.0.0.1:6379,defaultDatabase=10");
            RedisHelper.Initialization(cSRedisClient);
        }

        public override async Task<EmptyReply> register(RegisterRequest request, ServerCallContext context)
        {
            await cSRedisClient.SetAsync(request.Container, request.Ip);
            return new EmptyReply();
        }

        public override async Task<ServerReply> getServerIp(ServerRequest request, ServerCallContext context)
        {
            var ip = await cSRedisClient.GetAsync(request.ContainerId);
            if (ip == null)
            {
                ip = "";
            }
            return new ServerReply()
            {
                Ip = ip
            };
        }
    }
}
