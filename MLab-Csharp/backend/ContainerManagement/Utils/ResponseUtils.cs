using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace ContainerManagement.Utils
{
    public static class ResponseUtils
    {
        public class StandardResponse
        {
            public int Code { get; set; }
            public string Message { get; set; }
            public object Content { get; set; }
        }

        public static StandardResponse NewResponse(int code, string message, object content)
        {
            return new StandardResponse()
            {
                Code = code,
                Message = message,
                Content = content
            };
        }
    }
}
