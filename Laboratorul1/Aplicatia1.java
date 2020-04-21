
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import java.io.*;
import java.util.*;

public class Laborator1 {
    private File html;
    private String baseUri;
    private Document doc;
//------------------Aplicatia 1
    Laborator1(String htmlFile, String baseUri) throws IOException
    {

        html = new File(htmlFile);
        doc = Jsoup.parse(html, null, baseUri);
        this.baseUri = baseUri;
    }
//------------1.1
    private String getTitle() 
    {
        String title = doc.title();
        return title;
    }
//------------1.2
    private String getKeywords() 
    {
        Element keywords = doc.selectFirst("meta[name=keywords]");
        String keywordsString = "";
        if (keywords == null) {
            System.out.println("Nu exista!");
        } else {
            keywordsString = keywords.attr("content");
        }
        return keywordsString;
    }
//------------1.3
    private String getDescription()
    {
        Element description = doc.selectFirst("meta[name=description]");
        String descriptionString = "";
        if (description == null) {
            System.out.println("Nu exista!");
        } else {
            descriptionString = description.attr("content");
        }
        return descriptionString;
    }
//-------------1.4
    private String getRobots() 
    {
        Element robots = doc.selectFirst("meta[name=robots]");
        String robotsString = "";
        if (robots == null) {
            System.out.println("Nu exista!");
        } else {
            robotsString = robots.attr("content");
        }
        return robotsString;
    }

}
