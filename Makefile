.PHONY: help setup test validate version bump-version bump-major bump-minor bump-patch clean

# Default target
.DEFAULT_GOAL := help

# Read current version from VERSION file
VERSION := $(shell cat VERSION 2>/dev/null || echo "0.0.0")

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)⚒️  The Forge - Build System$(NC)"
	@echo ""
	@echo "$(GREEN)Available targets:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Current version:$(NC) $(VERSION)"

setup: ## Initialize repository (submodules, symlinks, plugins)
	@echo "$(BLUE)⚒️  Setting up The Forge...$(NC)"
	@./scripts/setup.sh
	@echo "$(GREEN)✓ Setup complete$(NC)"

test: ## Run all tests (Layer 1 only)
	@echo "$(BLUE)🧪 Running tests...$(NC)"
	@cd forge-plugin && bash tests/run_all.sh
	@echo "$(GREEN)✓ Tests complete$(NC)"

test-full: ## Run all tests (Layer 1 + Layer 2)
	@echo "$(BLUE)🧪 Running full test suite...$(NC)"
	@cd forge-plugin && bash tests/run_all.sh --layer2
	@echo "$(GREEN)✓ Full tests complete$(NC)"

test-e2e: ## Run all tests including E2E (requires claude CLI)
	@echo "$(BLUE)🧪 Running complete test suite with E2E...$(NC)"
	@cd forge-plugin && bash tests/run_all.sh --e2e
	@echo "$(GREEN)✓ Complete tests finished$(NC)"

validate: ## Validate plugins, symlinks, and hooks
	@echo "$(BLUE)🔍 Validating Forge components...$(NC)"
	@./scripts/verify-symlinks.sh
	@./scripts/validate-plugins.sh
	@echo "$(GREEN)✓ Validation complete$(NC)"

fix-symlinks: ## Fix broken symlinks
	@echo "$(BLUE)🔧 Fixing symlinks...$(NC)"
	@./scripts/fix-symlinks.sh
	@echo "$(GREEN)✓ Symlinks fixed$(NC)"

version: ## Show current version
	@echo "$(GREEN)Current version:$(NC) $(VERSION)"

bump-version: ## Bump version (usage: make bump-version VERSION=0.3.0-alpha)
	@if [ -z "$(NEW_VERSION)" ]; then \
		echo "$(RED)Error: NEW_VERSION not specified$(NC)"; \
		echo "Usage: make bump-version NEW_VERSION=x.y.z-alpha"; \
		exit 1; \
	fi
	@echo "$(BLUE)⚒️  Bumping version from $(VERSION) to $(NEW_VERSION)...$(NC)"
	@./scripts/bump-version.sh $(NEW_VERSION)
	@echo "$(GREEN)✓ Version bumped to $(NEW_VERSION)$(NC)"

bump-major: ## Bump major version (x.0.0)
	@echo "$(BLUE)⚒️  Bumping major version...$(NC)"
	@NEW_VERSION=$$(echo $(VERSION) | awk -F. -v OFS=. '{$$1=$$1+1; $$2=0; $$3=0; print}' | sed 's/-alpha//'); \
	./scripts/bump-version.sh $$NEW_VERSION-alpha
	@echo "$(GREEN)✓ Major version bumped$(NC)"

bump-minor: ## Bump minor version (x.y.0)
	@echo "$(BLUE)⚒️  Bumping minor version...$(NC)"
	@NEW_VERSION=$$(echo $(VERSION) | awk -F. -v OFS=. '{$$2=$$2+1; $$3=0; print}' | sed 's/-alpha//'); \
	./scripts/bump-version.sh $$NEW_VERSION-alpha
	@echo "$(GREEN)✓ Minor version bumped$(NC)"

bump-patch: ## Bump patch version (x.y.z)
	@echo "$(BLUE)⚒️  Bumping patch version...$(NC)"
	@NEW_VERSION=$$(echo $(VERSION) | awk -F. -v OFS=. '{$$3=$$3+1; print}' | sed 's/-alpha//'); \
	./scripts/bump-version.sh $$NEW_VERSION-alpha
	@echo "$(GREEN)✓ Patch version bumped$(NC)"

clean: ## Clean generated files and runtime artifacts
	@echo "$(BLUE)🧹 Cleaning generated files...$(NC)"
	@rm -rf .forge/
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@find . -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✓ Clean complete$(NC)"

install: ## Install The Forge as a Claude Code plugin (local)
	@echo "$(BLUE)⚒️  Installing The Forge locally...$(NC)"
	@cd forge-plugin && claude plugin install .
	@echo "$(GREEN)✓ Plugin installed$(NC)"

uninstall: ## Uninstall The Forge plugin
	@echo "$(BLUE)🗑️  Uninstalling The Forge...$(NC)"
	@claude plugin uninstall forge-plugin
	@echo "$(GREEN)✓ Plugin uninstalled$(NC)"

status: ## Show repository status (version, git, submodules)
	@echo "$(BLUE)⚒️  The Forge Status$(NC)"
	@echo ""
	@echo "$(YELLOW)Version:$(NC) $(VERSION)"
	@echo "$(YELLOW)Git branch:$(NC) $$(git rev-parse --abbrev-ref HEAD)"
	@echo "$(YELLOW)Git status:$(NC)"
	@git status -s
	@echo ""
	@echo "$(YELLOW)Submodules:$(NC)"
	@git submodule status
	@echo ""
	@echo "$(YELLOW)Symlinks:$(NC)"
	@./scripts/verify-symlinks.sh --quiet && echo "  $(GREEN)✓ All symlinks healthy$(NC)" || echo "  $(RED)✗ Some symlinks broken$(NC)"
