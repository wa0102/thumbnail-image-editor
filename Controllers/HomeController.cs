using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;

public class HomeController : Controller
{
    public IActionResult Index()
    {
        return View();
    }

    [HttpPost]
    public IActionResult Index(IFormFile image)
    {
        if (image == null || image.Length == 0)
        {
            TempData["Message"] = "画像が選択されていません。";
            return View();
        }

        var uploadsPath = Path.Combine(Directory.GetCurrentDirectory(), "wwwroot/uploads");
        if (!Directory.Exists(uploadsPath)) Directory.CreateDirectory(uploadsPath);

        var fileName = DateTime.Now.ToString("yyyyMMddHHmmssfff") + Path.GetExtension(image.FileName);
        var filePath = Path.Combine(uploadsPath, fileName);

        using (var stream = new FileStream(filePath, FileMode.Create))
        {
            image.CopyTo(stream);
        }

        ViewBag.ImageUrl = "/uploads/" + fileName;
        TempData["Message"] = "画像を保存しました！";

        var pythonExe = "python";
        var scriptPath = Path.Combine(Directory.GetCurrentDirectory(), "python", "remove_bg.py");
        var outputFileName = Path.GetFileNameWithoutExtension(fileName) + "_thumb.png";
        var outputFilePath = Path.Combine(uploadsPath, outputFileName);

        var psi = new ProcessStartInfo
        {
            FileName = pythonExe,
            Arguments = $"\"{scriptPath}\" \"{filePath}\" \"{outputFilePath}\"",
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            CreateNoWindow = true
        };

        using (var process = Process.Start(psi))
        {
            var output = process.StandardOutput.ReadToEnd();
            var error = process.StandardError.ReadToEnd();
            process.WaitForExit();

            if (!string.IsNullOrEmpty(error))
            {
                TempData["Message"] = "Pythonエラー: " + error;
                return View();
            }
        }

        ViewBag.ThumbImageUrl = "/uploads/" + outputFileName;

        return View();
    }
}
