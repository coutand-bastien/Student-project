package source;

import java.io.Serializable;

public class Normal implements SocialClass,Serializable {
	private String name;

	public Normal() {
		super();
		this.name = "normal";
	}

	public String getName() {return this.name; }
	public double reduction() {
		return 1;
	}	
}

