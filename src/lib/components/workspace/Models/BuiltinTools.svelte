<script lang="ts">
	import type i18nType from '$lib/i18n';
	import { getContext } from 'svelte';
	import Checkbox from '$lib/components/common/Checkbox.svelte';
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import ChevronDown from '$lib/components/icons/ChevronDown.svelte';
	import ChevronRight from '$lib/components/icons/ChevronRight.svelte';
	import { marked } from 'marked';
	import { BUILTIN_FUNCTION_LABELS, BUILTIN_TOOL_DEFINITIONS } from './builtinToolDefinitions';

	const i18n: typeof i18nType = getContext('i18n');

	const toolLabels = BUILTIN_TOOL_DEFINITIONS;
	const functionLabels = BUILTIN_FUNCTION_LABELS;
	const toolFunctions = Object.fromEntries(
		Object.entries(toolLabels)
			.filter(([, definition]) => definition.functions)
			.map(([tool, definition]) => [tool, definition.functions])
	);

	type BuiltinToolValue = boolean | Record<string, boolean>;
	type BuiltinToolsConfig = Record<string, BuiltinToolValue>;

	const allTools = Object.keys(toolLabels) as Array<keyof typeof toolLabels>;
	let expandedTools: Record<string, boolean> = {};

	export let builtinTools: BuiltinToolsConfig = {};

	const getFunctionSettings = (tool: string): Record<string, boolean> => {
		const value = builtinTools[`${tool}Functions`];
		return typeof value === 'object' && value !== null ? value : {};
	};

	const isFunctionEnabled = (tool: string, functionName: string) => {
		return getFunctionSettings(tool)[functionName] !== false;
	};

	const setFunctionState = (tool: string, functionName: string, checked: boolean) => {
		const key = `${tool}Functions`;
		const settings = { ...getFunctionSettings(tool) };

		if (checked) {
			delete settings[functionName];
		} else {
			settings[functionName] = false;
		}

		if (Object.keys(settings).length > 0) {
			builtinTools[key] = settings;
		} else {
			delete builtinTools[key];
		}

		builtinTools = { ...builtinTools };
	};
</script>

<div>
	<div class="mb-1.5 text-xs text-gray-400 dark:text-gray-600">{$i18n.t('Builtin Tools')}</div>
	<div class="grid grid-cols-1 items-start gap-x-5 gap-y-1 sm:grid-cols-2 lg:grid-cols-3">
		{#each allTools as tool}
			<div class="min-w-0">
				<div class="flex min-h-6 items-center justify-between gap-2.5">
					<div class="flex min-w-0 items-center gap-1 text-xs text-gray-600 dark:text-gray-400">
						{#if toolFunctions[tool]}
							<button
								type="button"
								class="flex size-4 shrink-0 items-center justify-center rounded hover:bg-gray-100 dark:hover:bg-gray-800"
								aria-label={$i18n.t('Functions')}
								on:click={() => {
									expandedTools = { ...expandedTools, [tool]: !expandedTools[tool] };
								}}
							>
								{#if expandedTools[tool]}
									<ChevronDown className="size-3" />
								{:else}
									<ChevronRight className="size-3" />
								{/if}
							</button>
						{/if}
						<Tooltip content={marked.parse(toolLabels[tool].description)}>
							<span class="truncate">{$i18n.t(toolLabels[tool].label)}</span>
						</Tooltip>
					</div>
					<Checkbox
						ariaLabel={$i18n.t(toolLabels[tool].label)}
						state={builtinTools[tool] !== false ? 'checked' : 'unchecked'}
						on:change={(e) => {
							if (e.detail === 'checked') {
								delete builtinTools[tool];
							} else {
								builtinTools[tool] = false;
							}
							builtinTools = { ...builtinTools };
						}}
					/>
				</div>

				{#if toolFunctions[tool] && expandedTools[tool]}
					<div class="ml-2 mt-1 space-y-1 border-l border-gray-100 pl-2 dark:border-gray-800">
						{#each toolFunctions[tool] ?? [] as functionName}
							<div class="flex min-h-6 items-center justify-between gap-2.5">
								<Tooltip content={marked.parse(`\`${functionName}\``)}>
									<span
										class="min-w-0 truncate text-[11px] text-gray-500 dark:text-gray-500"
										class:opacity-50={builtinTools[tool] === false}
										>{$i18n.t(functionLabels[functionName] ?? functionName)}</span
									>
								</Tooltip>
								<Checkbox
									ariaLabel={$i18n.t(functionLabels[functionName] ?? functionName)}
									disabled={builtinTools[tool] === false}
									state={isFunctionEnabled(tool, functionName) ? 'checked' : 'unchecked'}
									on:change={(e) => {
										setFunctionState(tool, functionName, e.detail === 'checked');
									}}
								/>
							</div>
						{/each}
					</div>
				{/if}
			</div>
		{/each}
	</div>
</div>
