<script lang="ts">
	import { getContext } from 'svelte';
	import Checkbox from '$lib/components/common/Checkbox.svelte';
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import ChevronDown from '$lib/components/icons/ChevronDown.svelte';
	import ChevronRight from '$lib/components/icons/ChevronRight.svelte';
	import { marked } from 'marked';

	const i18n = getContext('i18n');

	const toolLabels = {
		time: {
			label: $i18n.t('Time & Calculation'),
			description: $i18n.t('Get current time and perform date/time calculations')
		},
		memory: {
			label: $i18n.t('Memory'),
			description: $i18n.t('Search and manage user memories')
		},
		chats: {
			label: $i18n.t('Chat History'),
			description: $i18n.t('Search and view user chat history')
		},
		notes: {
			label: $i18n.t('Notes'),
			description: $i18n.t('Search, view, and manage user notes')
		},
		knowledge: {
			label: $i18n.t('Knowledge Base'),
			description: $i18n.t('Browse and query knowledge bases')
		},
		files: {
			label: $i18n.t('Files'),
			description: $i18n.t('List, search, and read files attached to the current chat')
		},
		channels: {
			label: $i18n.t('Channels'),
			description: $i18n.t('Search channels and channel messages')
		},
		notifications: {
			label: $i18n.t('Notifications'),
			description: $i18n.t('Send notifications to configured webhook targets')
		},
		web_search: {
			label: $i18n.t('Web Search'),
			description: $i18n.t('Search the web and fetch URLs')
		},
		image_generation: {
			label: $i18n.t('Image Generation'),
			description: $i18n.t('Generate and edit images')
		},
		code_interpreter: {
			label: $i18n.t('Code Interpreter'),
			description: $i18n.t('Execute code')
		},
		tasks: {
			label: $i18n.t('Task Management'),
			description: $i18n.t('Break down complex requests into trackable steps')
		},
		automations: {
			label: $i18n.t('Automations'),
			description: $i18n.t('Create and manage scheduled automations')
		},
		calendar: {
			label: $i18n.t('Calendar'),
			description: $i18n.t('List calendars, search, create, update, and delete calendar events')
		},
		subagents: {
			label: $i18n.t('Sub-agents'),
			description: $i18n.t('Delegate focused work to parallel sub-agents')
		}
	};

	const functionLabels: Record<string, string> = {
		search_memories: 'Search memories',
		list_memory_paths: 'List memory paths',
		read_memory_path: 'Read memory path',
		list_memories: 'List memories',
		update_memory: 'Update memory',
		add_memory: 'Add memory',
		replace_memory_content: 'Replace memory content',
		delete_memory: 'Delete memory',
		list_knowledge_bases: 'List knowledge bases',
		search_knowledge_bases: 'Search knowledge bases',
		query_knowledge_bases: 'Query knowledge bases',
		list_knowledge: 'List knowledge',
		grep_knowledge_files: 'Grep knowledge files',
		search_knowledge_files: 'Search knowledge files',
		query_knowledge_files: 'Query knowledge files',
		view_knowledge_file: 'View knowledge file',
		view_file: 'View file',
		view_note: 'View note',
		kb_exec: 'KB exec'
	};

	const toolFunctions: Partial<Record<keyof typeof toolLabels, string[]>> = {
		memory: [
			'search_memories',
			'list_memory_paths',
			'read_memory_path',
			'list_memories',
			'update_memory',
			'add_memory',
			'replace_memory_content',
			'delete_memory'
		],
		knowledge: [
			'list_knowledge_bases',
			'search_knowledge_bases',
			'query_knowledge_bases',
			'list_knowledge',
			'grep_knowledge_files',
			'search_knowledge_files',
			'query_knowledge_files',
			'view_knowledge_file',
			'view_file',
			'view_note',
			'kb_exec'
		]
	};

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
