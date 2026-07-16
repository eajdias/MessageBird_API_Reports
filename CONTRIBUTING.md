# Contributing to Omnichannel Reporting Tool

Thank you for your interest in contributing to this project! We welcome contributions from the community to help improve the tool.

## How to Contribute

1.  **Report Bugs:** If you find a bug, please open an issue on the repository with a detailed description of the problem and steps to reproduce it.
2.  **Suggest Enhancements:** If you have ideas for new features or improvements, feel free to open an issue to discuss them.
3.  **Submit Pull Requests:**
    *   Fork the repository.
    *   Create a new branch for your changes.
    *   Ensure your code follows the project's architecture and coding standards (see `docs/arquitetura_e_desenvolvimento.md`).
    *   Add tests for your changes.
    *   Submit a pull request with a clear description of your changes.

## Coding Standards

*   Follow **Clean Architecture** principles.
*   Keep the domain layer pure (no external dependencies).
*   Use `uv` for dependency management.
*   Ensure all tests pass before submitting a pull request.
*   Use the AI skill system (`.opencode/skills/`) for specialized tasks:
    *   `arch-guard`: revisões arquiteturais e criação/refatoração de código.
    *   `report-architect`: evoluir Dashboards/Excel e exportadores.
    *   `sync-maintainer`: mexer na pipeline de sincronização MessageBird -> SQLite.
    *   `add-business-metric`: adicionar ou alterar métricas de negócio.
    *   `business-config`: adaptar a configuração para uma nova empresa.

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.
