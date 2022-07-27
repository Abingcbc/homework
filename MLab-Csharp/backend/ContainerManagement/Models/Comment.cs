using System;
using System.Collections.Generic;

namespace ContainerManagement.Models
{
    public partial class Comment
    {
        public int CommentId { get; set; }
        public int? PostId { get; set; }
        public string Username { get; set; }
        public string Content { get; set; }
        public DateTime? CreateTime { get; set; }
        public int? Status { get; set; }

        public virtual Post Post { get; set; }
        public virtual User UsernameNavigation { get; set; }
    }
}
