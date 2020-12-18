package source;

import java.io.Serializable;

public class Zero implements SocialClass,Serializable{
	private String name;

    public Zero() {
		super();
		this.name = "zero";
	}

	public String getName() { return this.name; }
	public double reduction() { return 0; }
}
