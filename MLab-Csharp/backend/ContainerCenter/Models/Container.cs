using System;
using System.Collections.Generic;

namespace ContainerCenter.Models
{
    public class Container
    {
        public int ContainerId { get; set; }
        public string Username { get; set; }
        public string ContainerName { get; set; }
        public int? Type { get; set; }
        public DateTime? CreateTime { get; set; }
    }
}
