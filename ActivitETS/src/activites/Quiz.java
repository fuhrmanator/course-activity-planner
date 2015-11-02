package activites;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.LocalDateTime;
import java.util.Calendar;
import java.util.Date;
import java.util.TimeZone;

public class Quiz {

	
	private int id;
	private String nom;
	private String nomFichier;
	private String path;
	private String resume;
	private LocalDateTime dateOpen;
	private LocalDateTime dateClose;
	TimeZone timeZone = TimeZone.getDefault();
	
	public Quiz(int id, String nomFichier, String path) {
		//super(nom, nomFichier);
		this.id =id;
		this.nomFichier = nomFichier;
		this.path = path;
	}
	
	/*public Quiz(int id, String nom, String resume, Calendar dateStart, Calendar dateStop) {
		//super(nom, nomFichier);
		id =id;
		resume = resume;
		dateStart = dateStart;
		dateStop = dateStop;
	}*/

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getNom() {
		return nom;
	}

	public void setNom(String nom) {
		this.nom = nom;
	}

	public String getResume() {
		return resume;
	}

	public void setResume(String resume) {
		this.resume = resume;
	}

	public LocalDateTime getDateStart() {
		return dateOpen;
	}

	public void setDateStart(LocalDateTime date) {
		
	    dateOpen = date;
		
	}

	public LocalDateTime getDateStop() {
		return dateClose;
	}

	public void setDateStop(LocalDateTime date) {
		dateClose = date;	
	}
	
	
	public String getNomFichier() {
		return nomFichier;
	}

	public void setNomFichier(String nomFichier) {
		this.nomFichier = nomFichier;
	}

	public String getPath() {
		return path;
	}

	public void setPath(String path) {
		this.path = path;
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

	public String toString() {
		
		return "id : " + id + " //name : " + nom + " //resume : " + resume + " //dateStart : " + dateOpen + " //dateStop : " + dateClose;
	}
	
	
}
