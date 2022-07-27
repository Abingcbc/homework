using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Community.Models;
using Community.Utils;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using static ResponseUtils.ResponseUtils;

namespace Community.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class CommentsController : ControllerBase
    {
        private readonly MyDbContext _context;

        public CommentsController(MyDbContext context)
        {
            _context = context;
        }

        // GET: api/Comments/5
        [HttpGet("{id}")]
        public ActionResult<StandardResponse> GetComment(int id)
        {
            var Comment = _context.Comment.Where(c => c.PostId == id);

            return NewResponse(200, "success", Comment);
        }

        // Post: api/Comments
        [HttpPost]
        public async Task<ActionResult<StandardResponse>> CommentComment(Comment comment)
        {
            _context.Comment.Add(comment);
            var commentNum = _context.Post.Find(comment.PostId).CommentNum;
            _context.Post.Find(comment.PostId).CommentNum = commentNum + 1;
            await _context.SaveChangesAsync();
            return NewResponse(200, "success", comment);
        }

        // DELETE: api/Comments/5
        [HttpDelete("{id}")]
        public async Task<ActionResult<StandardResponse>> DeleteComment(int id)
        {
            var comment = await _context.Comment.FindAsync(id);
            if (comment == null)
            {
                return NotFound();
            }

            _context.Comment.Remove(comment);
            var commentNum = _context.Post.Find(comment.PostId).CommentNum;
            _context.Post.Find(comment.PostId).CommentNum = commentNum - 1;
            await _context.SaveChangesAsync();

            return NewResponse(200, "success", null);
        }

        private bool CommentExists(int id)
        {
            return _context.Comment.Any(e => e.CommentId == id);
        }
    }
}
