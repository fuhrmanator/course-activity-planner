package activites;

import java.io.File;
import java.time.LocalDateTime;

public class Activite {

	private String nomFichier;
	private String nom;
	private LocalDateTime dateOpen;
	private LocalDateTime dateClose;
	
	public Activite(String type, String nomFichier, String nom) {
		nomFichier = nomFichier;
		dateOpen = null;
		dateClose = null;
		nom = nom.split("_")[0];
	}

	public String getNomFichier() {
		return nomFichier;
	}

	public void setNomFichier(String nomFichier) {
		this.nomFichier = nomFichier;
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

	public String getNom() {
		return nom;
	}

	public void setNom(String nom) {
		this.nom = nom;
	}

}
