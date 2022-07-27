using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Community.Models;
using Community.Utils;
using static ResponseUtils.ResponseUtils;

namespace Community.Controllers
{
    [Route("api")]
    [ApiController]
    public class UsersController : ControllerBase
    {
        private readonly MyDbContext _context;

        public UsersController(MyDbContext context)
        {
            _context = context;
        }

        // POST: api/login
        [Route("login")]
        [HttpPost]
        public async Task<ActionResult<StandardResponse>> Login(User user)
        {
            var userDB = await _context.User.FindAsync(user.Username);

            if (userDB == null)
            {
                return NewResponse(200, "fail", "No such user");
            }
            if (userDB.Password == TokenHelper.EnocdePWD(user.Password))
            {
                var token = TokenHelper.Encode(user.Username, user.Password);
                return NewResponse(200, "success", token);
            } else
            {
                return NewResponse(200, "fail", "Wrong password");
            }
        }

        // POST: api/register
        [Route("register")]
        [HttpPost]
        public async Task<ActionResult<StandardResponse>> Register(User user)
        {
            user.Password = TokenHelper.EnocdePWD(user.Password);
            _context.User.Add(user);
            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateException)
            {
                if (UserExists(user.Username))
                {
                    return NewResponse(200, "fail", "Conflict");
                }
                else
                {
                    return NewResponse(200, "fail", "Error");
                }
            }
            var token = TokenHelper.Encode(user.Username, user.Password);
            return NewResponse(200, "success", token);
        }

        private bool UserExists(string id)
        {
            return _context.User.Any(e => e.Username == id);
        }
    }
}
