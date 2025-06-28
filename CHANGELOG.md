# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.2.2] - 2025-06-28

### Added
 - **Updated models list**: Added more LLM models

## [0.2.1] - 2025-06-27

### Added
 - **Change to README.md**: Better support for instructions


## [0.2.0] - 2025-06-27

### Added
- **New OpenAI Models**: Support for latest OpenAI models including:
  - `gpt-4o` - Multimodal flagship model with vision capabilities
  - `gpt-4o-mini` - Economical model with great performance-to-cost ratio
  - `gpt-4.1` - Latest generation with 1M token context window
  - `gpt-4.1-mini`, `gpt-4.1-nano` - Smaller variants (estimated pricing)
  - `gpt-image-1` - Specialized vision model for image processing

- **New Anthropic Models**: Support for latest Claude models including:
  - `claude-sonnet-4` - Next generation Sonnet model
  - `claude-opus-4` - Next generation Opus model (estimated pricing)
  - `claude-3-7-sonnet` - Improved Sonnet variant

- **New Google Models**: Extended Gemini model support including:
  - `gemini-2.5-pro` - Latest generation Pro model with enhanced capabilities
  - `gemini-2.5-flash` - Faster variant of 2.5 generation
  - `gemini-2.5-flash-lite` - Lightweight flash model optimized for speed

- **Enhanced Testing**: Comprehensive test suite for all new models
- **Demo Scripts**: New examples demonstrating latest model capabilities
- **Documentation Updates**: README.md updated with current model support matrix

### Changed
- Updated pricing information for all models based on 2024-2025 rates
- Improved cost comparison examples in documentation
- Enhanced error handling for new model configurations

### Technical Details
- All new models use appropriate tokenizers (tiktoken for OpenAI, estimation for others)
- Large context models (1M+ tokens) properly supported
- Cost estimation updated with latest pricing tiers
- Full backward compatibility maintained

## [0.1.0] - Initial Release
- Basic token counting for OpenAI models
- Support for GPT-3.5 and GPT-4 families
- Claude 3 model support
- Basic Gemini model support
- File and console logging
- Cost estimation functionality
