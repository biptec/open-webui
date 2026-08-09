<script lang="ts">
	import CodeBracket from '$lib/components/icons/CodeBracket.svelte';
	import Grid from '$lib/components/icons/Grid.svelte';
	import Wrench from '$lib/components/icons/Wrench.svelte';

	export let name = '';
	export let className = 'size-4';
	export let strokeWidth = '1.75';

	$: normalizedName = name.trim().toLowerCase();
</script>

{#if normalizedName.includes('playwright')}
	<Grid {className} {strokeWidth} />
{:else if normalizedName.includes('coder')}
	<CodeBracket {className} {strokeWidth} />
{:else}
	<Wrench {className} {strokeWidth} />
{/if}
