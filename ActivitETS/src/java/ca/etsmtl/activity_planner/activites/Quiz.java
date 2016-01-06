package ca.etsmtl.activity_planner.activites;

import java.time.LocalDateTime;
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

	@Override
	public String getNom() {
		return nom;
	}

	@Override
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


	@Override
	public String getNomFichier() {
		return nomFichier;
	}

	@Override
	public void setNomFichier(String nomFichier) {
		this.nomFichier = nomFichier;
	}

	public String getPath() {
		return path;
	}

	public void setPath(String path) {
		this.path = path;
	}

	@Override
	public LocalDateTime getDateOpen() {
		return dateOpen;
	}

	@Override
	public void setDateOpen(LocalDateTime dateOpen) {
		this.dateOpen = dateOpen;
	}

	@Override
	public LocalDateTime getDateClose() {
		return dateClose;
	}

	@Override
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

	@Override
	public String toString() {

		return "id : " + id + " //name : " + nom + " //resume : " + resume + " //dateStart : " + dateOpen + " //dateStop : " + dateClose;
	}


}
