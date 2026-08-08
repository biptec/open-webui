<script lang="ts">
	import type i18nType from '$lib/i18n';
	import { getContext, onMount } from 'svelte';
	import ChevronDown from '$lib/components/icons/ChevronDown.svelte';
	import ChevronRight from '$lib/components/icons/ChevronRight.svelte';
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import { getTerminalServers, type TerminalServer } from '$lib/apis/terminal';
	import { BUILTIN_TOOL_DEFINITIONS } from './builtinToolDefinitions';

	const i18n: typeof i18nType = getContext('i18n');

	type Tool = {
		id: string;
		name?: string;
		meta?: { description?: string };
	};

	type InstructionItem = {
		id: string;
		name: string;
		description: string;
		kind: string;
	};

	export let toolInstructions: Record<string, string> = {};
	export let builtinTools: Record<string, boolean | Record<string, boolean>> = {};
	export let builtinEnabled = true;
	export let tools: Tool[] = [];
	export let terminalId = '';
	export let terminalEnabled = true;
	export let showAllBuiltins = false;

	let terminals: TerminalServer[] = [];
	let expanded: Record<string, boolean> = {};

	onMount(async () => {
		terminals = await getTerminalServers(localStorage.token);
	});

	const setInstruction = (id: string, value: string) => {
		const next = { ...toolInstructions };
		if (value.trim() === '') {
			delete next[id];
		} else {
			next[id] = value;
		}
		toolInstructions = next;
	};

	const getToolKind = (id: string) => {
		if (id.startsWith('server:mcp:')) return 'MCP';
		if (id.startsWith('server:')) return 'OpenAPI';
		return 'Tool';
	};

	$: instructionItems = (() => {
		const items: InstructionItem[] = [];

		if (builtinEnabled || showAllBuiltins) {
			for (const [id, definition] of Object.entries(BUILTIN_TOOL_DEFINITIONS)) {
				if (!showAllBuiltins && builtinTools[id] === false) continue;
				items.push({
					id: `builtin:${id}`,
					name: $i18n.t(definition.label),
					description: $i18n.t(definition.description),
					kind: $i18n.t('Builtin')
				});
			}
		}

		// Keep instructions configurable for tools that can be enabled later from the chat UI.
		for (const tool of tools) {
			const id = tool.id;
			items.push({
				id: `tool:${id}`,
				name: tool?.name || id,
				description: tool?.meta?.description || id,
				kind: getToolKind(id)
			});
		}

		if (terminalEnabled && terminalId) {
			const terminal = terminals.find((item) => item.id === terminalId);
			items.push({
				id: `terminal:${terminalId}`,
				name: terminal?.name || terminalId,
				description: terminal?.url || terminalId,
				kind: $i18n.t('Terminal')
			});
		}

		return items;
	})();
</script>

{#if instructionItems.length > 0}
	<div>
		<div class="mb-1.5 flex items-center justify-between gap-2">
			<div class="text-xs text-gray-400 dark:text-gray-600">{$i18n.t('Tool Instructions')}</div>
			<div class="text-[11px] text-gray-400 dark:text-gray-600">
				{instructionItems.length}
				{$i18n.t('available')}
			</div>
		</div>

		<div class="space-y-1">
			{#each instructionItems as item (item.id)}
				<div class="rounded-lg border border-gray-100/80 dark:border-gray-850/80">
					<button
						type="button"
						class="flex w-full items-center justify-between gap-3 px-2.5 py-2 text-left"
						on:click={() => {
							expanded = { ...expanded, [item.id]: !expanded[item.id] };
						}}
					>
						<div class="flex min-w-0 items-center gap-2">
							{#if expanded[item.id]}
								<ChevronDown className="size-3 shrink-0" />
							{:else}
								<ChevronRight className="size-3 shrink-0" />
							{/if}
							<Tooltip content={item.description}>
								<span class="truncate text-xs text-gray-700 dark:text-gray-300">{item.name}</span>
							</Tooltip>
							<span class="shrink-0 text-[10px] text-gray-400 dark:text-gray-600">{item.kind}</span>
						</div>
						{#if toolInstructions[item.id]?.trim()}
							<span class="shrink-0 text-[10px] text-gray-500 dark:text-gray-500"
								>{$i18n.t('Custom')}</span
							>
						{/if}
					</button>

					{#if expanded[item.id]}
						<div class="border-t border-gray-100/80 px-2.5 py-2 dark:border-gray-850/80">
							<textarea
								class="min-h-20 w-full resize-y bg-transparent text-xs text-gray-700 outline-hidden placeholder:text-gray-300 dark:text-gray-300 dark:placeholder:text-gray-700"
								placeholder={$i18n.t(
									'Describe when to use this tool, when not to use it, and any tool-specific rules.'
								)}
								value={toolInstructions[item.id] ?? ''}
								on:input={(event) => {
									setInstruction(item.id, (event.currentTarget as HTMLTextAreaElement).value);
								}}
							></textarea>
							<div class="mt-1 text-[10px] text-gray-400 dark:text-gray-600">
								{$i18n.t('Applied only when this tool is available to the model.')}
							</div>
						</div>
					{/if}
				</div>
			{/each}
		</div>
	</div>
{/if}
