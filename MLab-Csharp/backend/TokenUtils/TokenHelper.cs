using JWT.Algorithms;
using JWT.Builder;
using System;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Text;

namespace TokenUtils
{
    public static class TokenHelper
    {
        private static JwtBuilder builder = new JwtBuilder();
        private static MD5 mD5 = MD5.Create();
        private static string secret = "secret";

        public static string Encode(string username, string password)
        {
            return builder.WithAlgorithm(new HMACSHA256Algorithm())
                .WithSecret(secret)
                .AddClaim("username", username)
                .AddClaim("password", password)
                .Encode();
        }

        public static string Decode(string token)
        {
            return builder.WithAlgorithm(new HMACSHA256Algorithm())
                .WithSecret(secret)
                .Decode(token);
        }

        public static string EnocdePWD(string password)
        {
            byte[] byteOld = Encoding.UTF8.GetBytes(password);
            byte[] byteNew = mD5.ComputeHash(byteOld);
            StringBuilder encodedPWD = new StringBuilder();
            foreach (byte b in byteNew)
            {
                encodedPWD.Append(b.ToString("x2"));
            }
            return password.ToString();
        }
    }
}
