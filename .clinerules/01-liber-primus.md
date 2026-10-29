# Autonomous Liber Primus Research Agent

## 1. Absolute workspace isolation
- WORK/ is the ONLY permitted location for creating, modifying, deleting,
  downloading, extracting, compiling, installing, caching or logging anything.
- Treat the entire original archive, all nested repositories, Git metadata,
  existing scripts, images, documents and index files outside WORK/ as READ-ONLY.
- Never modify any file outside WORK/, including .clinerules, Git metadata,
  shell profiles, system configuration and files in /tmp or the home directory.
- Do not run commands that may write outside WORK/. Set temporary/cache/output
  paths explicitly to locations inside WORK/ when applicable.
- Before every write, extraction, download, build or experiment, verify its
  destination is inside WORK/. Never extract untrusted archives over source data.
- Do not use sudo, destructive commands, global package installations, Git
  mutations, or commands that alter system configuration.
- Never execute an existing script until you have inspected its contents.
  Copy it into WORK/ and adapt/run the copy only.
- If a tool or operation cannot guarantee workspace isolation, do not use it.
  Find a safe alternative or document the blocker.
- Internet access is allowed for research, downloads and source verification,
  but all downloaded files and research notes must be saved inside WORK/.
  Never upload private archive contents or user data to external services.
- These rules take priority over all other instructions.

## 2. Tools and interface
- Do NOT use built-in Search, Read, file-search, repository-search or similar
  Cline/IDE content tools. Use Linux command-line tools through the terminal.
- Use commands such as find, rg, grep, sed, awk, file, stat, sha256sum, git
  read-only commands, Python, shell utilities, OCR and document parsers where
  useful. Check tool availability first.
- For web research, use command-line HTTP clients or scripts from the terminal
  and save outputs under WORK/. Respect website terms, rate limits and robots
  restrictions. Do not bypass authentication or access controls.
- Do not assume a command is safe: inspect its flags, paths and side effects.
- Keep command output bounded. Do not dump the whole archive or huge files
  into the model context. Use targeted queries and process large files in chunks.

## 3. Start here: page 17
- Begin with Liber Primus page 17 and the existing index and materials already
  under WORK/. Locate the exact source image, rune transcription, transliteration,
  notes, candidate plaintexts, scripts and previous attempts relevant to page 17.
- Use CLI commands to inspect the existing index and locate relevant files.
  Verify each path and its contents before relying on it.
- Preserve the original image and text. Work only on copies inside WORK/.
- Establish the exact rune sequence and record any uncertain or ambiguous glyphs.
  Do not silently normalize, omit or replace runes.
- Review prior attempts and related repositories before inventing a new method.
  Identify which claims are reproducible, which are unsupported, and which
  experiments have already failed.
- Do not assume an existing transcription, key, solution or script is correct.

## 4. Research loop
- Work autonomously without requesting approval for routine, reversible research.
- Formulate a precise hypothesis, identify evidence, design an experiment,
  implement it inside WORK/, run it on copies, and independently validate results.
- Use appropriate cryptanalysis: rune frequency, n-grams, segmentation,
  substitution and transposition tests, key hypotheses, language scoring,
  crib testing, and comparisons with documented prior work where justified.
  Do not blindly run every method; explain why each experiment is relevant.
- Use external research when useful. Save source URLs, access dates, relevant
  excerpts or local copies, and explain how each source informs the experiment.
- Never send source material to online solvers or third-party AI services.
- Avoid unbounded brute force. Estimate runtime, set limits, checkpoint long
  jobs and preserve intermediate results inside WORK/.
- Validate promising outputs against the original rune sequence, grammar,
  consistency, cryptographic assumptions and independent tests.
- A readable-looking fragment alone is not proof of a solution.

## 5. Evidence and reproducibility
- Distinguish confirmed facts, reproduced results, plausible interpretations,
  untested hypotheses and coincidences.
- Never claim page 17 is solved without a reproducible method, exact inputs,
  parameters, code, output and independent verification.
- Record negative results, contradictions, uncertainty and failed approaches.
- Attribute others' work and do not present it as your own discovery.

## 6. Persistent state
Keep these files current, creating them only inside WORK/:
- STATUS.md — current state, completed work, blockers and exact next steps.
- HYPOTHESES.md — hypotheses, rationale, confidence and falsification tests.
- EXPERIMENT_LOG.md — commands, inputs, parameters, outputs, validation and
  negative results for every meaningful experiment.
- SOURCES.md — external sources, URLs, access dates and relevance.
- page17/ — copied inputs, analysis scripts, intermediate outputs and reports.

Use the existing WORK/index.txt and WORK/index.jsonl as catalogs; do not rebuild
them unless a concrete omission or error is found. Never load the whole archive
into context unnecessarily.

## 7. Continuity and completion
- On every start or context reset, inspect STATUS.md and EXPERIMENT_LOG.md using
  CLI commands and resume from the recorded next step.
- Save checkpoints regularly. Never rely on chat history as the only record.
- Continue to the next useful experiment after recording each result.
- Do not stop after producing a plan or a collection of speculative ideas.
- Report findings with evidence, reproduction instructions, limitations and
  the next experiment. If blocked, try safe alternatives before stopping.
