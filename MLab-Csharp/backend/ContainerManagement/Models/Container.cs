using System;
using System.Collections.Generic;

namespace ContainerManagement.Models
{
    public partial class Container
    {
        public Container()
        {
            Post = new HashSet<Post>();
        }

        public int ContainerId { get; set; }
        public string Username { get; set; }
        public string ContainerName { get; set; }
        public DateTime? CreateTime { get; set; }
        public int? Type { get; set; }

        public virtual User UsernameNavigation { get; set; }
        public virtual ICollection<Post> Post { get; set; }
    }
}
