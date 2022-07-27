using System;
using System.Collections.Generic;

namespace ContainerManagement.Models
{
    public partial class User
    {
        public User()
        {
            Comment = new HashSet<Comment>();
            Container = new HashSet<Container>();
            Likes = new HashSet<Likes>();
            Post = new HashSet<Post>();
        }

        public string Username { get; set; }
        public string Password { get; set; }

        public virtual ICollection<Comment> Comment { get; set; }
        public virtual ICollection<Container> Container { get; set; }
        public virtual ICollection<Likes> Likes { get; set; }
        public virtual ICollection<Post> Post { get; set; }
    }
}
