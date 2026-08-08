export type BuiltinToolDefinition = {
	label: string;
	description: string;
	functions?: string[];
};

export const BUILTIN_TOOL_DEFINITIONS: Record<string, BuiltinToolDefinition> = {
	time: {
		label: 'Time & Calculation',
		description: 'Get current time and perform date/time calculations'
	},
	memory: {
		label: 'Memory',
		description: 'Search and manage user memories',
		functions: [
			'search_memories',
			'list_memory_paths',
			'read_memory_path',
			'list_memories',
			'update_memory',
			'add_memory',
			'replace_memory_content',
			'delete_memory'
		]
	},
	chats: {
		label: 'Chat History',
		description: 'Search and view user chat history'
	},
	notes: {
		label: 'Notes',
		description: 'Search, view, and manage user notes'
	},
	knowledge: {
		label: 'Knowledge Base',
		description: 'Browse and query knowledge bases',
		functions: [
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
	},
	files: {
		label: 'Files',
		description: 'List, search, and read files attached to the current chat'
	},
	channels: {
		label: 'Channels',
		description: 'Search channels and channel messages'
	},
	notifications: {
		label: 'Notifications',
		description: 'Send notifications to configured webhook targets'
	},
	web_search: {
		label: 'Web Search',
		description: 'Search the web and fetch URLs'
	},
	image_generation: {
		label: 'Image Generation',
		description: 'Generate and edit images'
	},
	code_interpreter: {
		label: 'Code Interpreter',
		description: 'Execute code'
	},
	tasks: {
		label: 'Task Management',
		description: 'Break down complex requests into trackable steps'
	},
	automations: {
		label: 'Automations',
		description: 'Create and manage scheduled automations'
	},
	calendar: {
		label: 'Calendar',
		description: 'List calendars, search, create, update, and delete calendar events'
	},
	subagents: {
		label: 'Sub-agents',
		description: 'Delegate focused work to parallel sub-agents'
	}
};

export const BUILTIN_FUNCTION_LABELS: Record<string, string> = {
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
