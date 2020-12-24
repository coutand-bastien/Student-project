package source;

import java.io.Serializable;

public class Demie implements SocialClass, Serializable {
	private String name;

	public Demie() {
		super();
		this.name = "demie";
	}

	public String getName() {return this.name; }
	public double reduction() {
		return 0.5;
	}
	
	
}
