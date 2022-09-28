package oit;

import java.io.File;
import java.io.IOException;
import java.util.Iterator;
import java.util.List;

import org.apache.commons.io.FileUtils;

import com.github.dockerjava.api.command.InspectExecResponse.Container;
import com.github.dockerjava.api.command.PingCmd;
import com.github.dockerjava.core.DefaultDockerClientConfig;
import com.github.dockerjava.core.DefaultDockerClientConfig.Builder;
import com.github.dockerjava.core.DockerClientBuilder;
import com.github.dockerjava.core.DockerClientConfig;
import com.github.dockerjava.core.DockerClientImpl;
import com.github.dockerjava.httpclient5.ApacheDockerHttpClient;
import com.github.dockerjava.transport.DockerHttpClient;
import com.github.dockerjava.transport.DockerHttpClient.Request;
import com.github.dockerjava.transport.DockerHttpClient.Response;



public class DockerClient {
	
	
	public static void main(String[] args)  {
		
		DockerClientConfig standard = DefaultDockerClientConfig.createDefaultConfigBuilder()
				.withDockerHost("unix:///var/run/docker.sock")
				.build();
		
		

		DockerHttpClient httpClient = new ApacheDockerHttpClient.Builder()
				.dockerHost(standard.getDockerHost())
		    .build();
		
		
		// Local docker istance
		com.github.dockerjava.api.DockerClient dockerClient = DockerClientImpl.getInstance(standard, httpClient);
		
		
		// Images list
		List<com.github.dockerjava.api.model.Image> images = dockerClient.listImagesCmd().withShowAll(false).exec();
		Iterator<com.github.dockerjava.api.model.Image>  iteratorImage = images.iterator(); 
		
		System.out.println("Number of container: " + images.size());
		System.out.println("\n");

		System.out.println("---- Images list ----");
		
		while(iteratorImage.hasNext()) {
			
			com.github.dockerjava.api.model.Image image = iteratorImage.next();
			System.out.println(image.toString());
		
		}
		
		
		// Containers list
		List<com.github.dockerjava.api.model.Container> containers = dockerClient.listContainersCmd().withShowAll(true).exec();
		Iterator<com.github.dockerjava.api.model.Container>  iteratorConteiner = containers.iterator(); 
		
		System.out.println("\n");
		
		
		System.out.println("Number of container: " + containers.size());
		System.out.println("---- Containers list ----");
		
		while(iteratorConteiner.hasNext()) {
			
			com.github.dockerjava.api.model.Container container = iteratorConteiner.next();
			System.out.println(container.getImage() + " " + container.getStatus() + " " + container.getState());
		
		}
		
		// Create container from dockerfile
		File dockerFile = new File("/Users/nicolo.toscani/Desktop/Dockerfile");
		String dockerParse;
		
		try {
			
			dockerParse = FileUtils.readFileToString(dockerFile, "UTF-8");
			System.out.println(dockerParse);
		
		} catch (IOException e) {
			
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		System.out.print(" --- Durante l'attesa pausa paglia ---");
		System.out.print("\n");
		
		dockerClient.buildImageCmd(dockerFile)
		.withTag("demo")
		.exec(null);
		
		System.out.print("Image created");
		
	}

}
