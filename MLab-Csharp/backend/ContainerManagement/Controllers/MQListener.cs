using ContainerCenter;
using ContainerManagement.Models;
using CSRedis;
using Docker.DotNet;
using Docker.DotNet.Models;
using FluentScheduler;
using Grpc.Net.Client;
using Microsoft.Extensions.Hosting;
using Newtonsoft.Json;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;


namespace ContainerManagement.Controllers
{
    public class MQListener : BackgroundService
    {
        private IConnection connection;
        private IModel channel;
        private DockerClient client;
        private ContainerService.ContainerServiceClient gRpcClient;
        private CSRedisClient cSRedisClient;

        public MQListener()
        {
            var connectionFactory = new ConnectionFactory()
            {
                HostName = MyConfig.MqHostName,
                UserName = MyConfig.MqUsername,
                Password = MyConfig.MqPassword
            };
            connection = connectionFactory.CreateConnection();
            channel = connection.CreateModel();
            channel.BasicQos(0, 1, false);
            client = new DockerClientConfiguration(new Uri("http://localhost:2375")).CreateClient();
            var gRpcChannel = GrpcChannel.ForAddress("https://localhost:12000");
            gRpcClient = new ContainerService.ContainerServiceClient(gRpcChannel);
            cSRedisClient = new CSRedisClient("127.0.0.1:6379,defaultDatabase=11");
            RedisHelper.Initialization(cSRedisClient);
        }

        // 启动时，向容器中心注册
        [Obsolete]
#pragma warning disable CS0809 // 过时成员重写未过时成员
        public override async Task StartAsync(CancellationToken cancellationToken)
#pragma warning restore CS0809 // 过时成员重写未过时成员
        {
            //string ip = Dns.GetHostByName(Dns.GetHostName()).AddressList[0].ToString();
            string ip = "127.0.0.1";
            var containerList = await client.Containers.ListContainersAsync(new ContainersListParameters()
            {
                All = true
            });
            //ATLSimpleObject aTLSimpleObject = new ATLSimpleObject();
            foreach (var container in containerList)
            {
                if (container.Names[0].Contains("mlab"))
                {
                    System.Diagnostics.Debug.WriteLine("register " + container.Names[0]);
                    gRpcClient.register(new RegisterRequest()
                    {
                        // 从docker中取出的名字会带一个 /
                        Container = container.Names[0].Substring(5),
                        Ip = ip
                    });
                }
            }
            var consumer = new EventingBasicConsumer(channel);
            System.Diagnostics.Debug.WriteLine("------------- register -------------");
            consumer.Received += async (ch, ea) =>
            {
                System.Diagnostics.Debug.WriteLine("------------- receive -------------");
                String message = Encoding.UTF8.GetString(ea.Body.Span);
                Container container = JsonConvert.DeserializeObject<Container>(message);
                string mHostPort = (20000 + container.ContainerId).ToString();
                var result = await client.Containers.CreateContainerAsync(new Docker.DotNet.Models.CreateContainerParameters()
                {
                    Image = container.Type == 0 ? "mlab-base" : "mlab-tensorflow",
                    Name = "mlab" + container.ContainerId.ToString(),
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
                cSRedisClient.Set(container.ContainerId.ToString(), mHostPort);
                gRpcClient.register(new RegisterRequest()
                {
                    Container = container.ContainerId.ToString(),
                    Ip = ip
                });
                channel.BasicAck(ea.DeliveryTag, false);
            };
            channel.BasicConsume("mlab", false, consumer);
            //BindingClass.getMemoryInfo();
            
        }

        class BindingClass
        {
            [DllImport(@"E:\Project\C#\MLab-Csharp\backend\Debug\SystemMonitor.dll", 
                CallingConvention = CallingConvention.StdCall)]
            public static extern string getMemoryInfo();

        }

        protected override Task ExecuteAsync(CancellationToken stoppingToken)
        {
            stoppingToken.ThrowIfCancellationRequested();
            return Task.CompletedTask;
        }

        public override void Dispose()
        {
            connection.Close();
            channel.Close();
            base.Dispose();
            client.Dispose();
        }

    }
}
