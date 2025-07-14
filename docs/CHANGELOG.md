# SUPERMODELS - CHANGELOG

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
