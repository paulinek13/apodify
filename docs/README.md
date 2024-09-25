# About

The goal of this project is to enhance APODs ([Astronomy Picture of the Day](https://apod.nasa.gov/)) with a primary focus on tailoring these enhancements specifically for the needs of **[neso](https://github.com/paulinek13/neso)**. To meet these needs, the project adds more detailed information to each **APOD** entry and implements advanced functionality, such as color-based searching and filtering. Every feature is designed with **neso** in mind, ensuring seamless integration and customization, but you can also use it for your own needs.

> [!NOTE]  
> This project is currently in active development and has not yet reached its first full release. There are some features that are still in progress or not yet implemented, and the documentation may be missing information.

# Configuration

By default all data is saved to a local SQLite database. This setup allows you to quickly start using the tool without needing external services. You can perform filtering, searching, and other operations directly within the local environment.

If you prefer to use **[Supabase](https://supabase.com/)** for storing data, you can enable it in the configuration settings. Keep in mind that **[apodify](https://github.com/paulinek13/apodify)** supports either a local SQLite database or **Supabase** — only one can be active at a time. #review

# Database

## Supabase

As this project is focused on enhancing **APODs** specifically for the **neso** web app, **Supabase** is utilized to store additional data related to **APODs**. The process is as follows:

1. **apodify** processes data from [NASA's APOD API](https://github.com/nasa/apod-api) and generates or extracts more detailed information for each **APOD** entry.
2. This enriched data is then uploaded to a specific table within a **Supabase** instance, enabling **neso** to easily retrieve the information via API calls.

## SQLite

In addition to integrating with **Supabase** for storing and retrieving enhanced **APOD** data, **apodify** also supports saving data to a local SQLite database. This feature allows for efficient filtering and searching of **APOD** entries directly within the local environment, without relying on external services.

# Versioning

**apodify** follows **[Semantic Versioning](https://semver.org/)** for its versioning system. For each major version, a new local SQLite database will be created, or a new **Supabase** table will need to be set up. This approach is due to the lack of planned database migrations.

Please see [CHANGELOG](CHANGELOG.md) and [VERSIONS](VERSIONS.md) for more details.