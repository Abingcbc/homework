using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.WebSockets;
using System.Runtime.InteropServices;
using System.Threading.Tasks;
using ContainerManagement.Controllers;
using ContainerManagement.Models;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

namespace ContainerManagement
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddControllers();
            services.AddDbContext<MyDbContext>();
            services.AddHostedService<MQListener>();
            //var database = "Graphite";
            //var uri = new Uri("http://127.0.0.1:8086");

            //services.AddMetrics(options =>
            //{
            //    options.GlobalTags.Add("app", "mlab");
            //    options.GlobalTags.Add("env", "stage");
            //})
            //   .AddHealthChecks()
            //   .AddJsonSerialization()
            //   .AddReporting(
            //      factory =>
            //      {
            //          factory.AddInfluxDb(
            //    new InfluxDBReporterSettings
            //    {
            //        InfluxDbSettings = new InfluxDBSettings(database, uri),
            //        ReportInterval = TimeSpan.FromSeconds(5)
            //    });
            //      })
            //   .AddMetricsMiddleware(options => options.IgnoredHttpStatusCodes = new[] { 404 });
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {

            //app.UseMetrics();
            //app.UseMetricsReporting(lifetime);
            ////loggerFactory.AddDebug();

            //if (env.IsDevelopment())
            //{
            //    app.UseDeveloperExceptionPage();
            //    app.UseBrowserLink();
            //}
            //else
            //{
            //    app.UseExceptionHandler("/Home/Error");
            //}
            //if (env.IsDevelopment())
            //{
            //    app.UseDeveloperExceptionPage();
            //}

            app.UseRouting();

            app.UseAuthorization();

            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllers();
            });
        }
    }
}
