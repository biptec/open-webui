import { WEBUI_API_BASE_URL } from '$lib/constants';
import type { Model } from '$lib/stores';

const preloadedModelImageUrls = new Set<string>();

export const getModelProfileImageUrl = (model: Model | null | undefined): string => {
	if (!model?.id) return '/favicon.png';

	const params = new URLSearchParams({ id: model.id });
	const updatedAt = model.info?.updated_at;
	if (updatedAt) params.set('v', String(updatedAt));

	return `${WEBUI_API_BASE_URL}/models/model/profile/image?${params.toString()}`;
};

export const preloadModelProfileImages = (models: (Model | null | undefined)[]) => {
	if (typeof Image === 'undefined') return;

	for (const model of models) {
		if (!model?.id) continue;
		const url = getModelProfileImageUrl(model);
		if (preloadedModelImageUrls.has(url)) continue;

		preloadedModelImageUrls.add(url);
		const image = new Image();
		image.src = url;
	}
};
