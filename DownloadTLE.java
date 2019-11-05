import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.CookieHandler;
import java.net.CookieManager;
import java.net.CookiePolicy;
import java.net.URL;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Scanner;

import javax.net.ssl.HttpsURLConnection;

public class DownloadTLE {

    /**
     * @param args
     */
    public static void main(String[] args) {
        try {
            String[] holder = new String[2];
            if (args.length == 0) {
                Scanner scan = new Scanner(System.in);
                System.out.println("Please key in username and password!");
                holder[0] = scan.nextLine();
                holder[1] = scan.nextLine();
                scan.close();
            } else if (args.length == 2) {
                holder = args;
            } else {
                System.out.println(
                    "Please enter the right username and password!\n" 
                    + "Exiting program!");
                return;
            }

            String baseURL = "https://www.space-track.org";
            String authPath = "/ajaxauth/login";
            String userName = holder[0];
            String password = holder[holder.length - 1];
            String query = "/basicspacedata/query/class/tle_latest/ORDINAL/1/EPOCH/%3Enow-30/orderby/NORAD_CAT_ID/format/3le";


            CookieManager manager = new CookieManager();
            manager.setCookiePolicy(CookiePolicy.ACCEPT_ALL);
            CookieHandler.setDefault(manager);

            URL url = new URL(baseURL+authPath);

            HttpsURLConnection conn = (HttpsURLConnection) url.openConnection();
            conn.setDoOutput(true);
            conn.setRequestMethod("POST");

            String input = "identity="+userName+"&password="+password;

            OutputStream os = conn.getOutputStream();
            os.write(input.getBytes());
            os.flush();

            BufferedReader br = new BufferedReader(new InputStreamReader((conn.getInputStream())));

            String output;
            System.out.println("Output from Server .... \n");
            while ((output = br.readLine()) != null) {
                System.out.println(output);
            }

            url = new URL(baseURL + query);

            br = new BufferedReader(new InputStreamReader((url.openStream())));
            
            ArrayList<String> lines = new ArrayList<>();
            System.out.println("ITS WORKING!!");
            while ((output = br.readLine()) != null) {
                lines.add(output);
            }

            Path path = Paths.get("data.text");
            Files.write(path, lines, StandardCharsets.UTF_8);

            url = new URL(baseURL + "/ajaxauth/logout");
            br = new BufferedReader(new InputStreamReader((url.openStream())));
            conn.disconnect();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}