import dotenv from 'dotenv';
import HiggsfieldAPI from './lib/HiggsfieldAPI.js';

// Load environment variables
dotenv.config();

// Initialize API with key from environment
const api = new HiggsfieldAPI(process.env.HIGGSFIELD_API_KEY);

async function generateVideos() {
    console.log('🎬 Starting video generation examples...\n');

    // Text-to-Video
    console.log('📝 Example 1: Text-to-Video Generation');
    const textResult = await api.generateTextToVideo('A cat playing with a ball', {
        duration: 10,
        seed: 42
    });

    // Image-to-Video
    console.log('\n📸 Example 2: Image-to-Video Generation');
    const imageResult = await api.generateImageToVideo(
        'The dog runs in the park',
        'https://example.com/my-dog.jpg',
        { duration: 10, seed: 123 }
    );

    // Soul Mode
    console.log('\n👥 Example 3: Soul Mode Generation');
    const soulResult = await api.generateSoulVideo(
        'A young woman and a monkey dancing together in a colorful house',
        [
            'https://example.com/woman-character.png',
            'https://example.com/monkey-character.png',
            'https://example.com/colorful-house.jpg'
        ]
    );

    console.log('\n' + '='.repeat(60));
    console.log('Monitoring generation status...');
    console.log('='.repeat(60) + '\n');

    // Wait for completion of each generation
    if (textResult.success) {
        console.log('✅ Text-to-video generation started:', textResult.generation_id);
        await waitForCompletion(textResult.generation_id);
    } else {
        console.log('❌ Text-to-video generation failed:', textResult.error);
    }

    if (imageResult.success) {
        console.log('\n✅ Image-to-video generation started:', imageResult.generation_id);
        await waitForCompletion(imageResult.generation_id);
    } else {
        console.log('\n❌ Image-to-video generation failed:', imageResult.error);
    }

    if (soulResult.success) {
        console.log('\n✅ Soul mode generation started:', soulResult.generation_id);
        await waitForCompletion(soulResult.generation_id);
    } else {
        console.log('\n❌ Soul mode generation failed:', soulResult.error);
    }

    console.log('\n🎉 All generations complete!');
}

async function waitForCompletion(generationId) {
    let status;
    do {
        await new Promise(resolve => setTimeout(resolve, 10000));
        status = await api.getStatus(generationId);

        if (status.success === false) {
            console.log(`❌ ${generationId} - Error checking status:`, status.error);
            break;
        }

        console.log(`⏳ ${generationId} - Status: ${status.status} (${status.type})`);
    } while (['pending', 'in_queue', 'in_progress'].includes(status.status));

    if (status.status === 'completed') {
        console.log(`✨ Video completed: ${status.video_url}`);
        if (status.image_url) {
            console.log(`   Source image: ${status.image_url}`);
        }
        if (status.reference_image_urls) {
            console.log(`   Reference images: ${status.reference_images_count} images`);
        }
    } else if (status.status === 'failed') {
        console.log(`❌ Generation failed:`, status.error || 'Unknown error');
    }
}

// Check if API key is configured
if (!process.env.HIGGSFIELD_API_KEY) {
    console.error('❌ Error: HIGGSFIELD_API_KEY not found in environment variables');
    console.error('Please create a .env file with your API key:');
    console.error('HIGGSFIELD_API_KEY=your_api_key_here');
    process.exit(1);
}

// Run the examples
generateVideos().catch(error => {
    console.error('❌ Fatal error:', error);
    process.exit(1);
});
