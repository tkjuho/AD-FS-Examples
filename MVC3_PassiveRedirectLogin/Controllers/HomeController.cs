using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using Microsoft.IdentityModel.Claims;

namespace MVC3_PassiveRedirectLogin.Controllers
{
    public class HomeController : Controller
    {
        //
        // GET: /Home/
        public ActionResult Index()
        {
            var claimsPrincipal = System.Threading.Thread.CurrentPrincipal as IClaimsPrincipal;
            var claimsIdentity = (IClaimsIdentity)claimsPrincipal.Identity;

            var pairs = new Dictionary<string, string>();
            foreach (Claim claim in claimsIdentity.Claims)
            {
                pairs.Add(claim.ClaimType, claim.Value);
            }

            return View(pairs);
        }

    }
}
