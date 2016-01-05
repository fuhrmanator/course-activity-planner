package ca.etsmtl.activity_planner.activites;

import java.time.LocalDateTime;
import java.util.Comparator;

/*
 * projet : ActivitETS
 * @author : Denis BRESSAND
 * Date : 17/12/2015
 *
 * Objet Cours
 */


public class Cours implements Comparable<Cours> {

	private LocalDateTime dateStart;
	private LocalDateTime dateStop;
	private String description;
	private String location;
	private String sommaire;

	public Cours(LocalDateTime dateStart, LocalDateTime dateStop, String description, String location, String sommaire) {
		this.dateStart = dateStart;
		this.dateStop = dateStop;
		this.description = description;
		this.location = location;
		this.sommaire = sommaire;
	}

	public LocalDateTime getDateStart() {
		return dateStart;
	}

	public void setDateStart(LocalDateTime dateStart) {
		this.dateStart = dateStart;
	}

	public LocalDateTime getDateStop() {
		return dateStop;
	}

	public void setDateStop(LocalDateTime dateStop) {
		this.dateStop = dateStop;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public String getLocation() {
		return location;
	}

	public void setLocation(String location) {
		this.location = location;
	}

	public String getSommaire() {
		return sommaire;
	}

	public void setSommaire(String sommaire) {
		this.sommaire = sommaire;
	}

	@Override
	public String toString() {
		return this.sommaire;
	}

	public static Comparator<Cours> CoursComparator = new Comparator<Cours>() {


		@Override
		public int compare(Cours cours1, Cours cours2) {

			String sommaireCours1 = cours1.getSommaire();
			String sommaireCours2 = cours2.getSommaire();

			// ascending order
			return sommaireCours1.compareTo(sommaireCours2);
		}

	};

	@Override
	public int compareTo(Cours o) {
		// TODO Auto-generated method stub
		return 0;
	}
}
