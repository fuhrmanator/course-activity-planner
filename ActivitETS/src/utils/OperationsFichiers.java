package utils;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.time.Instant;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.TimeZone;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import javax.xml.transform.Result;
import javax.xml.transform.Source;
import javax.xml.transform.TransformerConfigurationException;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.TransformerFactoryConfigurationError;
import javax.xml.transform.sax.SAXSource;
import javax.xml.transform.stream.StreamResult;

import org.apache.commons.io.IOUtils;
import org.xml.sax.Attributes;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;
import org.xml.sax.helpers.XMLFilterImpl;
import org.xml.sax.helpers.XMLReaderFactory;

import activites.Activite;
import activites.Quiz;

/*
 * projet : ActivitETS
 * @author : Denis BRESSAND
 * Date : 17/12/2015
 * 
 * Classe permettant de parser les fichiers XML à l'aide de SAX Parser
 */


public class OperationsFichiers {

	private String quizName, quizResume;
	public static FileInputStream fis;
	private LocalDateTime dateOpen,dateClose;
	private Instant tsOpen, tsClose;
	TimeZone timeZone = TimeZone.getDefault();
	
	public OperationsFichiers() {
		
	}
	
	public ArrayList<Quiz> retournerListeActivites(File repertoire) {
		//ArrayList<Activite> listeActs = new ArrayList<Activite>();
		ArrayList<Quiz> listeQuizs = new ArrayList<Quiz>();
		String nomFic = "";
		String path = "";
				
		if ( repertoire.isDirectory ( ) ) {
            File[] list = repertoire.listFiles();

            for(int i = 0; i < list.length; ++i) {
            	if(list[i].getName().contains("quiz")) {
            		File ficXML = new File(list[i].getPath());
            		File[] listFicXML = ficXML.listFiles();

            		for(int j = 0; j < listFicXML.length; ++j) {
            			if(listFicXML[j].getName().contains("quiz")) {
                    		nomFic = listFicXML[j].getName();
                    		path = listFicXML[j].getPath();
            			}
            		}
                	listeQuizs.add(new Quiz(i, nomFic, path));
            	}
            	
            }
            /*if (list){
                for ( int i = 0; i < list.length; i++) {
                        // Appel récursif sur les sous-répertoires
                        listeRepertoire( list[i]);
                } 
            } else {
            	System.err.println(repertoire + " : Erreur de lecture.");
            }*/
    } 
		
		
		return listeQuizs;
	}

	public void lireFic(String path, Quiz quiz) {
		try {
			fis = new FileInputStream(path);
			//InputSource is = new InputSource(fis);

			//	 les fichier et récupere les dates
			//XMLFilterImpl xr = recupererDates();
			
			SAXParserFactory factory = SAXParserFactory.newInstance();
			SAXParser saxParser = factory.newSAXParser();
			
			DefaultHandler handler = new DefaultHandler()  {
				private String tagName = "";
				boolean dateOpenElement = false;
				boolean dateCloseElement = false;
				boolean quizNameBool = false;
				boolean quizResumeBool = false;

				@Override
				public void startElement(String uri, String localName,
						String qName, Attributes atts) throws SAXException {
					if (qName.equals("name")) {
						//System.out.println("name : " + qName);
						quizNameBool = true;
					}
					if (qName.equals("intro")) {
						//System.out.println("Resume : " + qName);
						quizResume = "";
						quizResumeBool = true;
					}
					if (qName.equals("timeopen")) {
						//System.out.println("Time open : " + qName);
						dateOpenElement = true;
					}
					if (qName.equals("timeclose")) {
						//System.out.println("Time close : " + qName);
						dateCloseElement = true;
					}
					super.startElement(uri, localName, qName, atts);
				}

				public void endElement(String uri, String localName,
						String qName) throws SAXException {
					if (qName.equals("name")) {
						quizNameBool = false;
					}
					if (qName.equals("intro")) {
						quizResumeBool = false;
					}
					if (qName.equals("timeopen")) {
						dateOpenElement = false;
					}
					if (qName.equals("timeclose")) {
						dateCloseElement = false;
					}
					super.endElement(uri, localName, qName);
				}

				@Override
				public void characters(char[] ch, int start, int length) throws SAXException {
					if(quizNameBool) {
						quizName = new String(ch, start, length);
					}
					if(quizResumeBool) {
						quizResume += new String(ch, start, length);
					}
					if(dateOpenElement) {
						tsOpen = Instant.ofEpochSecond(Long.parseLong(new String(ch, start, length)));
						dateOpen = LocalDateTime.ofInstant(tsOpen, ZoneId.systemDefault());
					}
					if(dateCloseElement) {
						tsClose = Instant.ofEpochSecond(Long.parseLong(new String(ch, start, length)));
						dateClose = LocalDateTime.ofInstant(tsClose, ZoneId.systemDefault());
					}
					super.characters(ch, start, length);
				}
			};
			
			saxParser.parse(path, handler);

		} catch (TransformerFactoryConfigurationError e2) {
			e2.printStackTrace();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (ParserConfigurationException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (SAXException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		quizResume = HTMLUtils.getDefault().getAsText(quizResume);
		quiz.setNom(quizName);
		quiz.setDateStart(dateOpen);
		quiz.setDateStop(dateClose);
		quiz.setResume(quizResume);
	}
	
	public void ecrireFichier(ArrayList<LocalDateTime> listesNewDates, String path) {
		
		try {			
			//fis = new FileInputStream(path);
			InputStream test = new FileInputStream(path);
			
			ByteArrayOutputStream baos = new ByteArrayOutputStream();

			// Fake code simulating the copy
			// You can generally do better with nio if you need...
			// And please, unlike me, do something about the Exceptions :D
			byte[] buffer = new byte[1024];
			int len;
			while ((len = test.read(buffer)) > -1 ) {
			    baos.write(buffer, 0, len);
			}
			baos.flush();

			// Open new InputStreams using the recorded bytes
			// Can be repeated as many times as you wish
			InputStream is1 = new ByteArrayInputStream(baos.toByteArray()); 
			
			InputSource is = new InputSource(is1);

			//les fichier et récupere les dates
			XMLFilterImpl xr = changeDates(listesNewDates);
			
			
			Source src = new SAXSource(xr, is);
			// Création du fichier de sortie
			//path = "C:\\Users\\Denis\\workspace\\ActivitETS\\MoodleBackup\\activities\\quiz_146043\\quiz5.xml";
			File file = new File(path);
			Result resultat = new StreamResult(file);

			TransformerFactory.newInstance().newTransformer().transform(src, resultat);
		} catch (TransformerConfigurationException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (TransformerException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (TransformerFactoryConfigurationError e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		
	}
	
	public XMLFilterImpl changeDates(ArrayList<LocalDateTime> listesNewDates) {
		XMLFilterImpl xr = null;
		try {
			xr = new XMLFilterImpl(XMLReaderFactory.createXMLReader()) {
				private String tagName = "";
				boolean dateOpenElement = false;
				boolean dateCloseElement = false;

				@Override
				public void startElement(String uri, String localName,
						String qName, Attributes atts) throws SAXException {
					
					if (qName.equals("timeopen")) {
						dateOpenElement = true;
					}
					if (qName.equals("timeclose")) {
						dateCloseElement = true;
					}
					super.startElement(uri, localName, qName, atts);
				}

				public void endElement(String uri, String localName,
						String qName) throws SAXException {
					
					if (qName.equals("timeopen")) {
						dateOpenElement = false;
					}
					if (qName.equals("timeclose")) {
						dateCloseElement = false;
					}
					super.endElement(uri, localName, qName);
				}

				@Override
				public void characters(char[] ch, int start, int length) throws SAXException {
					
					if(dateOpenElement) {
						
						ZoneId zoneId = ZoneId.systemDefault(); // or: ZoneId.of("Europe/Oslo");
						long epoch = listesNewDates.get(0).atZone(zoneId).toEpochSecond();
						ch = String.valueOf(epoch).toCharArray();
						start = 0;
						length = ch.length;
					}
					if(dateCloseElement) {
						
						ZoneId zoneId = ZoneId.systemDefault(); // or: ZoneId.of("Europe/Oslo");
						long epoch = listesNewDates.get(1).atZone(zoneId).toEpochSecond();
						ch = String.valueOf(epoch).toCharArray();
						start = 0;
						length = ch.length;
					}
					super.characters(ch, start, length);
				}
			};
		} catch (SAXException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		return xr;
	}

	public LocalDateTime getDateOpen() {
		return dateOpen;
	}

	public void setDateOpen(LocalDateTime dateOpen) {
		this.dateOpen = dateOpen;
	}

	public LocalDateTime getDateClose() {
		return dateClose;
	}

	public void setDateClose(LocalDateTime dateClose) {
		this.dateClose = dateClose;
	}

	public String getQuizName() {
		return quizName;
	}

	public void setQuizName(String quizName) {
		this.quizName = quizName;
	}

	public String getQuizResume() {
		return quizResume;
	}

	public void setQuizResume(String quizResume) {
		this.quizResume = quizResume;
	}
	
	
	
	

}
