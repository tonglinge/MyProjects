
public class SSHClient {
	
	public static String[] HOST = {"192.168.1.49","192.168.1.40"};
	
	public static String[] USER = {"tibco","tibco"};
	
	public static String[] PWD = {"tibco12","tibco12"};
	
	public static String[] SHELL = {"/home/tibco/shell-program/bin/uptime.sh tibco","/home/tibco/shell-program/bin/uptime.sh tibco"};
	
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		
		for(int i=0;i<HOST.length;i++)
		{
			SSHClientImpl.ssh(HOST[i],USER[i],PWD[i],SHELL[i]);
		}


	}

}
