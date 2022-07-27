using System;
using System.Collections.Generic;

namespace ContainerManagement.Models
{
    public partial class Post
    {
        public Post()
        {
            Comment = new HashSet<Comment>();
            Likes = new HashSet<Likes>();
        }

        public int PostId { get; set; }
        public string Username { get; set; }
        public string Title { get; set; }
        public int? ContainerId { get; set; }
        public string Content { get; set; }
        public DateTime? CreateTime { get; set; }
        public int? LikeNum { get; set; }
        public int? CommentNum { get; set; }
        public int? Status { get; set; }

        public virtual Container Container { get; set; }
        public virtual User UsernameNavigation { get; set; }
        public virtual ICollection<Comment> Comment { get; set; }
        public virtual ICollection<Likes> Likes { get; set; }
    }
}
