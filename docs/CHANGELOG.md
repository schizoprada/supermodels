# SUPERMODELS - CHANGELOG

## [0.1.18] -- *07/20/2025*
* Added framework-agnostic converter system for complex Python object serialization
* Implemented DataclassConverter for automatic dataclass ↔ JSON conversion with datetime field support
* Implemented PydanticConverter for Pydantic model serialization using built-in model_dump()
* Created SQLATypeAdapter for integrating converters with SQLAlchemy column types
* Added convenient factory methods: DCType for dataclasses, PydType for Pydantic models
* Enhanced type safety with ConversionTarget and ConversionOptions type aliases
* Structured converters as reusable components for future database adapter support

## [0.1.17] -- *07/15/2025*
* Enhanced Manager class with ergonomic initialization - supports both `Manager(adapter, User, Order)` and `Manager(adapter)(User, Order)` patterns
* Refactored registeroperations decorator into dedicated core/utils/decorators.py module for better organization
* Moved ManagerContext to core/models/contexts.py for improved code structure
* Extended BaseManager with dynamic operation registration and dispatch capabilities via @registeroperations decorator
* Added session management methods to BaseManager (close, commit, rollback)
* Implemented bulk operations for BaseManager (bulkadd, bulkupdate, bulkdelete)
* Added advanced query methods to BaseManager (getall, getone)
* Made bulk operations abstract methods in DBAdapter base class for consistent interface
* Improved type safety with proper overloads for registeroperations decorator
* Unified operation dispatch between ManagerContext and BaseManager while maintaining their distinct responsibilities

## [0.1.16] -- *07/15/2025*
* Renamed `supermodels` -> `supermodel`

## [0.1.15] -- *07/14/2025*
* Renamed `supermodels` -> `supermodel`

## [0.1.14] -- *07/14/2025*
* Added comprehensive documentation and docstrings throughout the codebase
* Implemented detailed exception messages with context for better debugging
* Created proper __init__ files with module exports and documentation
* Added complete package documentation with usage examples
* Improved error handling with descriptive messages for all edge cases
* Organized imports and exports for clean public API interface

## [0.1.13] -- *07/14/2025*
* Implemented concrete SQLAlchemy adapter with full DBAdapter interface
* Added SQLAlchemy session management with proper error handling and rollback
* Created pagination support with OrderBy enum and sorting capabilities
* Implemented bulk operations (bulkadd, bulkupdate, bulkdelete) for performance
* Added Manager factory methods and global default adapter support via __getitem__
* Created type-safe SQLAlchemy integration with Engine and sessionmaker support

## [0.1.12] -- *07/14/2025*
* Implemented Manager class with `*models` signature for dynamic model management
* Added ManagerContext for context-managed database operations
* Created dynamic method dispatch system - `mgr.add(item)` auto-detects model type
* Implemented @registeroperations decorator for automatic CRUD and custom operation registration
* Added support for custom model operations via `__super__` attribute
* Wired metaclass registry with runtime model lookup and validation
* Added comprehensive error handling for edge cases (unknown types, inheritance, unregistered models)
* Note: Test isolation issue exists when running full test suite due to decorator class modification - individual test files pass correctly

## [0.1.11] -- *07/14/2025*
* Implemented manager metaclass for automatic model registration
* Created model registry system for runtime type mapping
* Designed base manager class with dynamic model dispatch
* Completed base adapter abstract methods with proper signatures
* Added support for single and multiple model management per manager
* Fixed TypeVar covariance issues for protocol and adapter compatibility

## [0.1.0] -- *07/14/2025*
* Project Initialized
