using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Community.Models;
using static ResponseUtils.ResponseUtils;
using System.Collections;

namespace Community.Controllers
{
    [Route("api/[controller]/[action]")]
    [ApiController]
    public class LikesController : ControllerBase
    {
        private readonly MyDbContext _context;

        public LikesController(MyDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public ActionResult<StandardResponse> GetMyLikes(string username)
        {
            var likes = _context.Likes.Where(l => l.Username == username).ToList();
            var postList = new ArrayList();
            foreach (var like in likes)
            {
                postList.Add(_context.Post.Find(like.PostId));
            }
            return NewResponse(200, "success", postList);
        }

        [HttpGet]
        public ActionResult<StandardResponse> GetPostLikes(int postId)
        {
            var likes = _context.Likes.Where(l => l.PostId == postId).ToList();
            return NewResponse(200, "success", likes);
        }

        [HttpGet]
        public async Task<ActionResult<StandardResponse>> IsLiked(string username, int postId)
        {
            var postList = await _context.Likes
                .Where(l => l.Username == username && l.PostId == postId).ToListAsync();
            if (postList.Count > 0)
            {
                return NewResponse(200, "success", true);
            } else
            {
                return NewResponse(200, "success", false);
            }
        }

        [HttpPost]
        public async Task<ActionResult<StandardResponse>> NewLikes(Likes likes)
        {
            _context.Likes.Add(likes);
            var likeNum = _context.Post.Find(likes.PostId).LikeNum;
            _context.Post.Find(likes.PostId).LikeNum = likeNum + 1;
            await _context.SaveChangesAsync();

            return NewResponse(200, "success", likes);
        }

        [HttpPost]
        public async Task<ActionResult<StandardResponse>> DeleteLikes(Likes like)
        {
            var likes = await _context.Likes
                .Where(l => l.PostId == like.PostId && l.Username == like.Username).ToListAsync();
            if (likes.Count == 0)
            {
                return NotFound();
            }

            _context.Likes.Remove(likes[0]);
            var likeNum = _context.Post.Find(like.PostId).LikeNum;
            _context.Post.Find(like.PostId).LikeNum = likeNum - 1;
            await _context.SaveChangesAsync();

            return NewResponse(200, "success", null);
        }

        private bool LikesExists(int id)
        {
            return _context.Likes.Any(e => e.LikeId == id);
        }
    }
}
