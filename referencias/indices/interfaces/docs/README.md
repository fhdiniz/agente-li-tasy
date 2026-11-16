![](https://github.com/philips-internal/tasy-interfaces/actions/workflows/nightly-pipeline.yml/badge.svg)

# Tasy-Interfaces


Tasy-Interfaces platform intends to expose Tasy Standard APIs and custom interoperability interfaces.

The APIs and custom interfaces are available using REST. 

Tasy-Interfaces also provides an optional service that allows the interoperability from PL/SQL objects with the TIE Platform. 

Visit the [official Tasy-Interfaces sharepoint](https://share.philips.com/sites/ArchEMR/SitePages/Tasy-Interfaces.aspx) page to get access to the project documentation.

# Technical Diagram

![Tasy Interfaces Technical Diagram](docs/images/tasy-interfaces.png)

## Tasy-Interfaces and Integration Broker environments

Currently, Tasy-Interfaces APIs are just available for use by an Integration Broker. Nowadays TIE is the integration broker for Tasy.

It's important to mention that Tasy-Interfaces and TIE are not the same project. 

While Tasy-Interfaces intends to provide standard APIs and custom interfaces using REST, TIE is a decloupled interoperability platform. 

Tasy-Interfaces is part of Tasy, and follows the same Tasy versioning.

TIE has an independent documentation and versioning. 

To know more about TIE, visit the [TIE Sharepoint](https://share.philips.com/sites/Bifrost).


# Development environment

Tasy-Interfaces uses Gradle to build the project. It's suggested to use IntelliJ as IDE.

* Download the sources code (git) on your computer in any folder of your choice (create a branch based on the 'ART_<name>' branch).
* At the root of the tasy-interfaces project, run the 'gradlew build' command to compile the project and perform all necessary validations and tests.

```
gradlew build
```

## Configuration

### configuration.yml

To run Tasy-Interfaces, check the [server-app/configuration.yml](server-app/configuration.yml) file.

This file contains all the configurations available for Tasy-Interfaces. 

By default, it is configured to the TIE development environment [bifrostdev.whebdc.com.br].

If necessary, it is possible to start the application configured for another configuration.yml file using the following JVM argument:

``
-Dphilips.config.yaml.url = "file:/path/folder/configuration.yml"
``

### context.xml

This file contains the Tasy database that Tasy-Interfaces will connect.

* [server-app/src/main/webapp/META-INF/context.xml](server-app/src/main/webapp/META-INF/context.xml)

By default, it is configured for the Tasy development database [phdev].

## Running

To execute Tasy-Interfaces, the following command must be executed at the project root:

```
gradle appRun
```

To run in debug mode:

```
gradle appRunDebug
```

Tasy-interfaces runs on Tomcat 8.5.* and Weblogic 12.2.*. (Weblogic 12.1.* must be checked for retrocompatibility)

In this development environment by default it runs on tomcat:

* context: `/tasy-interfaces`
* port: `50001`
* debugPort: `5005`

These settings are in the file `gradle/tomcat.gradle`.

## Running with Authentication Enabled

When running tasy-interfaces with authentication enabled, the access to all the APIs will require an authentication token.

By default, the development environment is using the Philips Security Application available at [https://dev-tasy.whebdc.com.br/philips-security](https://dev-tasy.whebdc.com.br/philips-security).

You can use this instance for development purposes. If necessary, you can run a philips-security locally and change the tasy-interfaces authentication configurations in configuration.yml file.

![Tasy Interfaces Technical Diagram](docs/images/tasy-interfaces-authentication.png)


# Developing

All data exposed or received by Tasy-Interfaces must be defined in the most standard way possible, that is, it does not contain a reference to a specific client or integration name.
Except for exceptions, tasy-interfaces should only read and write data, having received them properly transformed. Data transformation is a task that must be done in the integration broker.
It is also highly recommended to avoid direct reference to specific details such as:

* Tasy database, such as column names in Portuguese, status values, etc.
* Message protocols, such as HL7 segment abbreviation, table domain, etc.
* The project is international and must be written in English.

# Release

Before committing your changes, run the command:

```
gradlew build
```

* Make sure that the build was successfully completed.
  * PMD 
  * Checkstyle 
  * SpotBugs


* Open a Pull Request for your ART_[name] branch.
* Verify that all required checks have been performed successfully.
* Your changes must be reviewed by an analyst and/or another developer.
* After everything is right, merge your changes.

# Review

* There should be no classes, documentation, methods, variables and other references other than in English.
* All markers in the PR description must be followed.

# How to trigger an integration event from Tasy

## Java

Example with a callback class.

```java

@Inject
private EventFactory factory;

public ExampleResult executeWithCallback() {

    ExampleArguments arguments = new ExampleArguments();
    arguments.setId("some value");

    Response response = factory.newEvent("event.name")
        .sync(true)
        .arguments(arguments)
        .dataCallback(ExampleCallback.class)
        .dispatch();
    
    return response.asObject(ExampleResult.class);
}

```

Example without a callback class.


```java

@Inject
private EventFactory factory;

public Map<String, Object> executeWithoutCallback() {
    
    Response response = factory.newEvent("event.name")
        .sync(true)
        .addToContentMap("name", "James Bond")
        .addToContentMap("age", "42")
        .dispatch();
    
    return response.asMap();
}
    
```


## PL / SQL

Integration shots via PL / SQL will always be asynchronous.

Using a callback class in tasy-interfaces to load the data to be sent in the integration:

```
SELECT BIFROST.SEND_INTEGRATION(
  'event.name',
  'com.philips.tasy.integration.serverapp.healthcheck.HealthCheckServiceCallback', 
  '{"healthCheckMessage": "Example"}'
) 
FROM DUAL
```

Without a callback class, with the data loaded from TASY:

```
SELECT SEND_INTEGRATION_CONTENT(
   'event.name', 
   '{"name" : "James Bond", "age" : 42}'
)
FROM DUAL
```

# API Documentation

## Class Naming Convention

Please ensure that the project classes have the following pattern:

Class Suffixes:

- *Resource: These sorts of classes are related to Endpoint exposition and Swagger Documentation. Do not contain business rules. 
- *Service: These sorts of classes are related to business rules. No endpoint exposition or swagger documentation is allowed here.

![Tags - Categories](docs/images/swagger/swagger_tag.PNG)

# Swagger Documentation

All the endpoints must be documented using swagger. 

* [Annotations](https://github.com/swagger-api/swagger-core/wiki/Swagger-2.X---Annotations)
* [Specification](https://swagger.io/specification/)

It's possible to run the local API documentation running the gradle task:

```
gradle copyAPIsLocalDocumentation
```

![API Documentation](docs/images/swagger/swagger_example_2.PNG)
![API Documentation](docs/images/swagger/swagger_example_3.PNG)

# Telemetry

Tasy-Interfaces can export traces, metrics, and logs via an [OpenTelemetry](https://opentelemetry.io/) javaagent attached to the Docker/Tomcat runtime. No manual instrumentation is required — auto-instrumentation covers JAX-RS/RESTEasy, Hibernate, JDBC, and the servlet layer.

It's **off by default** and only applies to the Docker/Tomcat deployment (not WebLogic, not local `gradlew appRun`).

## Enabling it

Set these environment variables on the container:

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `TASY_INTERFACES_TELEMETRY_ENABLED` | to turn it on | `false` | Attaches the OTel javaagent when `true` |
| `TASY_INTERFACES_OTEL_EXPORTER_OTLP_ENDPOINT` | **yes**, if enabled | — | OTLP/HTTP endpoint to export to. The container **refuses to start** if telemetry is enabled without this set. |
| `TASY_INTERFACES_OTEL_SERVICE_NAME` | no | `tasy-interfaces` | Reported as `OTEL_SERVICE_NAME` to the collector |
| `TASY_INTERFACES_OTEL_EXPORTER_OTLP_PROTOCOL` | no | `http/protobuf` | |
| `TASY_INTERFACES_OTEL_METRICS_EXPORTER` / `..._TRACES_EXPORTER` / `..._LOGS_EXPORTER` | no | `otlp` | |

## Notes

* The javaagent jar is fetched from Maven Central at Docker image build time and verified against a pinned SHA-256 checksum (`OTEL_JAVAAGENT_SHA256` build arg) — nothing is committed to the repo or resolved via Gradle for the production image. Bumping `OTEL_JAVAAGENT_VERSION` requires updating the checksum to match.
* Trace/span IDs already appear in the JSON logs automatically (Log4j2 context-data injection) — no extra configuration needed.
* This does not propagate a `traceparent` header back to API callers.

# Settings in Tasy

Tasy needs to communicate with tasy-interfaces to send events to TIE.
For this to occur, the following function parameters need to be filled:

* **10**: (YES / NO): Activates the system for sending integration events to tasy-interfaces.
* **11**: The path to tasy-interfaces (http: // ip: port / tasy-interfaces). In general, you must register for your user in Tasy the address for your computer, which is running tasy-interfaces. So you can test your code.
* **12**: integration method between tasy-interfaces and TIE. Default value: "H".
    * "H" (HTTP) <deprecated>: Oracle calls TIE direct using UTL_HTTP.REQ.
    * "P" (Polling): Tasy-interfaces will poll requests from Oracle and then calls TIE.
* **13**: Indicate the consumer name of the polling service (for Oracle requests). Tasy-interfaces will create all the requests with this consumer name, and tasy-interfaces instance can be configured in YML file to only consume requests with this consumer name.

![Image of parameters](docs/images/tasy_parameters.png)


# Polling Service

## Consumer Service

![Image of parameters](docs/images/polling01.png)

## Retry Service

![Image of parameters](docs/images/polling02.png)


