package utils;

import java.io.Reader;
import java.io.StringReader;

import javax.swing.text.html.HTMLDocument;
import javax.swing.text.html.HTMLEditorKit;

public class HTMLUtils {

	// private members
	private HTMLEditorKit kit = new HTMLEditorKit();
	private HTMLDocument doc = new HTMLDocument();

	// Default instance
	private static final HTMLUtils instance = new HTMLUtils();

	/** Create a new instance */
	public HTMLUtils() { /* do nothing */
	}

	/**
	 * Return a default shared-instance
	 * 
	 * @return default shared-instance
	 */
	public static HTMLUtils getDefault() {
		return instance;
	}

	/**
	 * Convert an HTML String to a simple-text (without tag)
	 * 
	 * @param html
	 *            well-formed html string
	 * @return simple-text resulting
	 */
	public synchronized String getAsText(String html) {
		try {
			// clear our document's contents
			doc.remove(0, doc.getLength());
			if (html == null || html.equals(""))
				return html;

			// change <br> tags to <p> since the kit doesn't convert by a new
			// line
			html = html.replaceAll("<[bB][rR][\\s]*[/]?>", "<p>");

			// use the editorKit for separate "attributes set" to
			// "text-contents" by managing the document
			Reader r = new StringReader(html);
			kit.read(r, doc, 0);

			// return only "text-contents" part from the document ignoring this
			// way all "attributes set"
			return doc.getText(0, doc.getLength()).trim();
		} catch (Exception e) {
			e.printStackTrace();
			return null;
		}
	}

}
