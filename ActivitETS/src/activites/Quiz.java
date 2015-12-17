package activites;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.LocalDateTime;
import java.util.Calendar;
import java.util.Date;
import java.util.TimeZone;

/*
 * projet : ActivitETS
 * @author : Denis BRESSAND
 * Date : 17/12/2015
 * 
 * Objet Quiz qui hérite de Activite
 */


public class Quiz extends Activite {

	
	private int id;
	private String nom;
	private String nomFichier;
	private String path;
	private String resume;
	private LocalDateTime dateOpen;
	private LocalDateTime dateClose;
	TimeZone timeZone = TimeZone.getDefault();
	private Cours coursDebut;
	private Cours coursFin;
	
	public Quiz(int id, String nomFichier, String path) {
		//super(nom, nomFichier);
		this.id =id;
		this.nomFichier = nomFichier;
		this.path = path;
	}
	
	public Quiz(int id, String nomFichier, String path, Cours coursDebut, Cours coursFin) {
		//super(nom, nomFichier);
		this.id =id;
		this.nomFichier = nomFichier;
		this.path = path;
		this.coursDebut = coursDebut;
		this.coursFin = coursFin;
	}
	

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

	public Cours getCoursDebut() {
		return coursDebut;
	}

	public void setCoursDebut(Cours coursDebut) {
		this.coursDebut = coursDebut;
	}

	public Cours getCoursFin() {
		return coursFin;
	}

	public void setCoursFin(Cours coursFin) {
		this.coursFin = coursFin;
	}

	public String toString() {
		
		return "id : " + id + " //name : " + nom + " //resume : " + resume + " //dateStart : " + dateOpen + " //dateStop : " + dateClose;
	}
	
	
}
