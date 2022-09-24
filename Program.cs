using System;
using System.IO;
using Docker.DotNet;
using Docker.DotNet.Models;
using ICSharpCode.SharpZipLib.Tar;

namespace oit_docker_gateway
{
    class Program
    {
        static async System.Threading.Tasks.Task Main(string[] args)
        {
   
            // Connect to default Docker engine on Windows
            DockerClient client = new DockerClientConfiguration(
                new Uri("npipe://./pipe/docker_engine"))
                 .CreateClient();

            // Build Docker image - this command creates a tar of the entire working directory and send it to the build daemon
            using var tarball = CreateTarballForDockerfileDirectory(@"C:/Users/Server/Desktop/src");

            var imageBuildParameters = new ImageBuildParameters
            {
               
            };

            // Build 
            using var responseStream = await client.Images.BuildImageFromDockerfileAsync(tarball, imageBuildParameters);
           
            // Start container with specific name
            // await client.Containers.StartContainerAsync("bold_heisenberg", new ContainerStartParameters());
        }


        private static Stream CreateTarballForDockerfileDirectory(string directory)
        {
            var tarball = new MemoryStream();
            var files = Directory.GetFiles(directory, "*.*", SearchOption.AllDirectories);

            using var archive = new TarOutputStream(tarball)
            {
                //Prevent the TarOutputStream from closing the underlying memory stream when done
                IsStreamOwner = false
            };

            foreach (var file in files)
            {
                //Replacing slashes as KyleGobel suggested and removing leading /
                string tarName = file.Substring(directory.Length).Replace('\\', '/').TrimStart('/');

                //Let's create the entry header
                var entry = TarEntry.CreateTarEntry(tarName);
                using var fileStream = File.OpenRead(file);
                entry.Size = fileStream.Length;
                archive.PutNextEntry(entry);

                //Now write the bytes of data
                byte[] localBuffer = new byte[32 * 1024];
                while (true)
                {
                    int numRead = fileStream.Read(localBuffer, 0, localBuffer.Length);
                    if (numRead <= 0)
                        break;

                    archive.Write(localBuffer, 0, numRead);
                }

                //Nothing more to do with this entry
                archive.CloseEntry();
            }
            archive.Close();

            //Reset the stream and return it, so it can be used by the caller
            tarball.Position = 0;
            return tarball;
        }
    }
}
