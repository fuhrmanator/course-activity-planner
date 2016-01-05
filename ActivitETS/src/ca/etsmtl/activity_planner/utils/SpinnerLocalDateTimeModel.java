package ca.etsmtl.activity_planner.utils;

import java.io.Serializable;
import java.time.LocalDateTime;
import java.time.chrono.ChronoLocalDateTime;
import java.time.temporal.TemporalUnit;
import java.util.Objects;

import javax.swing.AbstractSpinnerModel;

public class SpinnerLocalDateTimeModel extends AbstractSpinnerModel implements Serializable {
	  private Comparable<ChronoLocalDateTime<?>> start, end;
	  private ChronoLocalDateTime<?> value;
	  private TemporalUnit temporalUnit;

	  public SpinnerLocalDateTimeModel(
	      ChronoLocalDateTime<?> value,
	      Comparable<ChronoLocalDateTime<?>> start,
	      Comparable<ChronoLocalDateTime<?>> end,
	      TemporalUnit temporalUnit) {
	    super();
	    if (Objects.isNull(value)) {
	      throw new IllegalArgumentException("value is null");
	    }
	    if (Objects.nonNull(start) && start.compareTo(value) >= 0
	     || Objects.nonNull(end)   && end.compareTo(value)   <= 0) {
	      throw new IllegalArgumentException("(start <= value <= end) is false");
	    }
	    this.value = value;
	    this.start = start;
	    this.end = end;
	    this.temporalUnit = temporalUnit;
	  }

	  public void setStart(Comparable<ChronoLocalDateTime<?>> start) {
	    if (Objects.isNull(start) ? Objects.nonNull(this.start)
	                              : !Objects.equals(start, this.start)) {
	      this.start = start;
	      fireStateChanged();
	    }
	  }

	  public Comparable<ChronoLocalDateTime<?>> getStart() {
	    return start;
	  }

	  public void setEnd(Comparable<ChronoLocalDateTime<?>> end) {
	    if (Objects.isNull(end) ? Objects.nonNull(this.end)
	                            : !Objects.equals(end, this.end)) {
	      this.end = end;
	      fireStateChanged();
	    }
	  }

	  public Comparable<ChronoLocalDateTime<?>> getEnd() {
	    return end;
	  }

	  public void setTemporalUnit(TemporalUnit temporalUnit) {
	    if (temporalUnit != this.temporalUnit) {
	      this.temporalUnit = temporalUnit;
	      fireStateChanged();
	    }
	  }

	  public TemporalUnit getTemporalUnit() {
	    return temporalUnit;
	  }

	  @Override public Object getNextValue() {
	    //Calendar cal = Calendar.getInstance();
	    //cal.setTime(value.getTime());
	    //cal.add(calendarField, 1);
	    //Date next = cal.getTime();
	    ChronoLocalDateTime<?> next = value.plus(1, temporalUnit);
	    return Objects.isNull(end) || end.compareTo(next) >= 0 ? next : null;
	  }

	  @Override public Object getPreviousValue() {
	    //Calendar cal = Calendar.getInstance();
	    //cal.setTime(value.getTime());
	    //cal.add(calendarField, -1);
	    //Date prev = cal.getTime();
	    ChronoLocalDateTime<?> prev = value.minus(1, temporalUnit);
	    return Objects.isNull(start) || start.compareTo(prev) <= 0 ? prev : null;
	  }

	  public ChronoLocalDateTime<?> getLocalDateTime() {
	    return value;
	  }

	  @Override public Object getValue() {
	    return value;
	  }

	  @Override public void setValue(Object value) {
	    if (!(value instanceof ChronoLocalDateTime<?>)) {
	      throw new IllegalArgumentException("illegal value");
	    }
	    if (!value.equals(this.value)) {
	      this.value = (LocalDateTime) value;
	      fireStateChanged();
	    }
	  }
	}