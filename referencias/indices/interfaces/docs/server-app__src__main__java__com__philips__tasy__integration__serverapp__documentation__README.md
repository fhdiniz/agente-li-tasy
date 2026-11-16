# Important 

The "com.philips.tasy.integration.serverapp.documentation" package must be deprecated. 

It must still in code for compatibility reasons with TIE v1 and TIEv2 integrations documentation.

After the complete migration of integrations to TIEv3, this package must be removed from the codebase.

The implementation available in package "com.philips.tasy.integration.serverapp.openapi" must be considered the "source of truth" for swagger generation.

Before the complete deprecation of "com.philips.tasy.integration.serverapp.documentation" package,
these classes must be moved to the "com.philips.tasy.integration.serverapp.openapi" package:

- DocumentationJaxrsScanner.java 
- DocumentationApiResource.java: only @Path("/catalog") endpoint and related dependencies.

The related configurations must be removed from
- configuration.yml
- TasyInterfacesConfigs.java
- Docker image variables.
- App Manager manifest
