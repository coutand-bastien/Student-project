package source;

/**
 * we chose to put an interface where the members will inherit because it allows a greater expandability
 * of the code later, if one day we wanted to add new functionality.
 */
public interface SocialClass  {
	
	/**
	 * @role determine the tariff reduction according to the social status
	 * @return the reduction
	 */
	double reduction();
}
