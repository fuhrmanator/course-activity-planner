package ca.etsmtl.activity_planner.utils;

import java.io.FileInputStream;
import java.io.IOException;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Iterator;

import ca.etsmtl.activity_planner.activites.Cours;
import net.fortuna.ical4j.data.CalendarBuilder;
import net.fortuna.ical4j.data.ParserException;
import net.fortuna.ical4j.model.Calendar;
import net.fortuna.ical4j.model.Component;

public class ImportCours {

	public ArrayList<Cours> parseCalendar(String pathCalendrier) {
		ArrayList<Cours> listeCours = new ArrayList<>();
		try {
			FileInputStream fin = new FileInputStream(pathCalendrier);
			CalendarBuilder builder = new CalendarBuilder();
			Calendar calendar = builder.build(fin);

			for (Iterator i = calendar.getComponents().iterator(); i.hasNext();) {
				Component component = (Component) i.next();

				//Date debut
				String dStart = component.getProperties().getProperty("DTSTART").getValue();
				int anneeStart = Integer.parseInt(dStart.substring(0, 4));
				int moisStart = Integer.parseInt(dStart.substring(4, 6));
				int jourStart = Integer.parseInt(dStart.substring(6, 8));
				int heureStart = Integer.parseInt(dStart.substring(9, 11));
				int minuteStart = Integer.parseInt(dStart.substring(11, 13));
				int secondeStart = Integer.parseInt(dStart.substring(13, 15));
				LocalDateTime dateStart = LocalDateTime.of(anneeStart, moisStart, jourStart, heureStart, minuteStart, secondeStart);

				//Date fin
				String dStop = component.getProperties().getProperty("DTEND").getValue();
				int anneeStop = Integer.parseInt(dStop.substring(0, 4));
				int moisStop = Integer.parseInt(dStop.substring(4, 6));
				int jourStop = Integer.parseInt(dStop.substring(6, 8));
				int heureStop = Integer.parseInt(dStop.substring(9, 11));
				int minuteStop = Integer.parseInt(dStop.substring(11, 13));
				int secondeStop = Integer.parseInt(dStop.substring(13, 15));
				LocalDateTime dateStop = LocalDateTime.of(anneeStop, moisStop, jourStop, heureStop, minuteStop, secondeStop);


				String description = component.getProperties().getProperty("DESCRIPTION").getValue();
				String location = component.getProperties().getProperty("LOCATION").getValue();
				String sommaire = component.getProperties().getProperty("SUMMARY").getValue();

				listeCours.add(new Cours(dateStart, dateStop, description, location, sommaire));
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ParserException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		return listeCours;
	}
}
