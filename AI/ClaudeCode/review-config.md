# Project Review Configuration — FC Mobile (FCMA-Dev)

## Output Language

简体中文 (Simplified Chinese)

> 评审报告的所有结论、问题描述与最终结论均以此处配置的语言输出；技术标识符（文件路径、类名/方法名、配置键）保持原文。如需改为其它语言，修改本节即可（例如填 `English`）。

## Review Dimensions

### 1. Killswitch Consistency
- Killswitch definitions follow "last one wins" semantics: if a KS with the same `name` appears multiple times in the final merged list, the **last** entry completely replaces all previous ones.
- Global definitions are in `server/server-game/conf/application.conf` (the base `killswitch.settings = [...]`).
- Regional overrides are in `server/server-game/conf/{china,korea,vietnam,global}/application.conf` using `killswitch.settings = ${killswitch.settings} [...]` (appending to the global list).
- When reviewing KS changes: verify the final effective value matches the stated intent. Check all regional configs for consistency.
- Key fields: `name`, `clientKey`, `clientAware` (BEFORE_AUTH, AFTER_AUTH, BEFORE_AND_AFTER_AUTH, AUTH_SPECIALIZED), `globalDefaults` (enabled/visible arrays).
- `globalDefaults: { enabled: ["-ALL"] }` means the feature is **disabled** by default for all platforms.
- Removing `globalDefaults` or removing `enabled: ["-ALL"]` means the feature is **enabled** by default.

### 2. Regional Config Cross-Check
- Changes to one regional config should be checked against other regions to understand if the change is intentionally region-specific.
- SKUs: china, korea, vietnam, global (and sometimes japan).
- Regional configs should only contain overrides; duplicating the full global list is an anti-pattern that causes maintenance drift.

### 3. Proto/Domain Changes
- Proto files in `proto/src/` generate Java classes. Changes need `mvn generate-sources` or full build.
- If a proto field is added/removed, check all serialization/deserialization call sites.

### 4. Guice Module Registration
- New services/modules must be registered in `DefaultGuiceInjectorInitializer`.
- Check `@Inject` dependencies are satisfiable.

### 5. SentryWard Metrics
- New metrics classes need corresponding HOCON config in the regional `application.conf` files.
- Check `sentryward.metrics` section matches any new metric classes.

## File Pattern Rules

| Pattern | Special Attention |
|---------|-------------------|
| `conf/*/application.conf` | KS override semantics, HOCON syntax, cross-region consistency |
| `*.proto` | Backward compatibility, regeneration needed |
| `*Resource.java` | REST endpoint changes, path conflicts |
| `*Module.java` | Guice binding, missing dependencies |
| `*DAO.java` | SQL injection risk, transaction boundaries |
| `sql*/` | Migration ordering, rollback safety |

## Known Pitfalls

1. **KS "last wins" trap**: Adding a KS entry earlier in the list doesn't override a later one. Only the last entry for a given name takes effect.
2. **Regional config bloat**: Copying global KS entries into regional configs creates maintenance burden. Only add entries that differ from global.
3. **HOCON append syntax**: `${killswitch.settings} [...]` appends to the resolved value of `killswitch.settings` from all previously included files. Order of `include` directives matters.
4. **clientAware mismatch**: If a KS's `clientAware` differs between global and regional, the regional value wins but may confuse the client if it expects a different timing.
5. **Missing KS in code**: Some KS names are only used by config/optools and not directly referenced in Java code — this is valid for operational killswitches.
