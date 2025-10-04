import MangaDexClient from './lib/mangadex.js';
import { formatMangaInfo, formatChapterInfo, displayMangaInfo, displayChapterInfo, sleep, downloadChapterImages } from './lib/utils.js';

/**
 * Main application - Search for "Chainsaw Man" and display manga info, chapters, and details
 */
async function main() {
  const client = new MangaDexClient();

  // Get search query and optional chapter number from command-line arguments
  const searchQuery = process.argv[2] || 'Chainsaw Man';
  const targetChapterNumber = process.argv[3] ? process.argv[3] : null;

  // UUID regex pattern for manga ID detection
  const uuidPattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  const isSearchById = uuidPattern.test(searchQuery);

  try {
    console.log('╔════════════════════════════════════════════════════════════════════════════╗');
    console.log('║              MangaDex API Demo - Manga Downloader                          ║');
    console.log('╚════════════════════════════════════════════════════════════════════════════╝');

    let selectedManga;

    if (isSearchById) {
      // Step 1: Get manga by ID
      console.log(`\n🔍 Fetching manga by ID: ${searchQuery}`);
      if (targetChapterNumber) {
        console.log(`🎯 Looking for Chapter ${targetChapterNumber}`);
      }

      const manga = await client.getMangaById(searchQuery);
      const formattedManga = formatMangaInfo(manga);

      console.log('\n✅ Manga found!');
      console.log('\n' + '═'.repeat(80));
      console.log('MANGA DETAILS');
      console.log('═'.repeat(80));
      displayMangaInfo(formattedManga, 1);

      selectedManga = formattedManga;
    } else {
      // Step 1: Search for manga by name
      console.log(`\n📚 Searching for "${searchQuery}"...`);
      if (targetChapterNumber) {
        console.log(`🎯 Looking for Chapter ${targetChapterNumber}`);
      }
      const searchResults = await client.searchManga(searchQuery, { limit: 5 });

      if (searchResults.length === 0) {
        console.log('❌ No manga found matching the search query.');
        return;
      }

      console.log(`\n✅ Found ${searchResults.length} manga matching "${searchQuery}"`);

      // Display all search results
      console.log('\n' + '═'.repeat(80));
      console.log('SEARCH RESULTS');
      console.log('═'.repeat(80));

      const formattedResults = searchResults.map(manga => formatMangaInfo(manga));
      formattedResults.forEach((manga, index) => {
        displayMangaInfo(manga, index + 1);
      });

      // Select the first manga (most relevant)
      selectedManga = formattedResults[0];
    }

    console.log('\n' + '═'.repeat(80));
    console.log(`📖 Selected: ${selectedManga.title} (ID: ${selectedManga.id})`);
    console.log('═'.repeat(80));

    // Add delay to respect rate limits
    await sleep(250);

    // Step 2: Get chapters for the selected manga
    console.log('\n📑 Fetching chapters...');
    let chapters;

    if (targetChapterNumber) {
      // Fetch recent 200 chapters when searching for specific chapter
      console.log('⏳ Fetching recent chapters...');
      chapters = await client.getMangaChapters(selectedManga.id, {
        language: 'en',
        limit: 200,
        order: 'desc'
      });
    } else {
      // Fetch only latest 10 chapters for general browsing
      chapters = await client.getMangaChapters(selectedManga.id, {
        language: 'en',
        limit: 10,
        order: 'desc'
      });
    }

    if (chapters.length === 0) {
      console.log('❌ No chapters found for this manga.');
      return;
    }

    const formattedChapters = chapters
      .map(chapter => formatChapterInfo(chapter))
      .filter(chapter => chapter.pages >= 10); // Filter out chapters with less than 10 pages

    // Determine which chapters to show in detail
    let chaptersToDetail;

    // If searching for a specific chapter
    if (targetChapterNumber) {
      const foundChapters = formattedChapters.filter(ch => ch.chapter === targetChapterNumber);

      if (foundChapters.length === 0) {
        console.log(`\n❌ Chapter ${targetChapterNumber} not found.`);
        console.log(`\n💡 Available chapters range: ${formattedChapters[0]?.chapter || 'N/A'} - ${formattedChapters[formattedChapters.length - 1]?.chapter || 'N/A'}`);
        console.log(`   Total chapters fetched: ${formattedChapters.length}`);
        return;
      }

      console.log(`\n✅ Found ${foundChapters.length} version(s) of Chapter ${targetChapterNumber}`);

      // Display found chapter(s)
      console.log('\n' + '═'.repeat(80));
      console.log(`CHAPTER ${targetChapterNumber} - AVAILABLE VERSIONS`);
      console.log('═'.repeat(80) + '\n');

      foundChapters.forEach((chapter, index) => {
        displayChapterInfo(chapter, index + 1);
        console.log('');
      });

      // Get detailed info for the found chapter(s)
      console.log('\n' + '═'.repeat(80));
      console.log(`DETAILED INFORMATION FOR CHAPTER ${targetChapterNumber}`);
      console.log('═'.repeat(80));

      chaptersToDetail = foundChapters;
    } else {
      // Original behavior: show first 20 chapters
      console.log(`\n✅ Found ${chapters.length} chapters (showing first ${Math.min(20, chapters.length)} in English)`);

      // Display chapter list
      console.log('\n' + '═'.repeat(80));
      console.log('CHAPTER LIST');
      console.log('═'.repeat(80) + '\n');

      const displayChapters = formattedChapters.slice(0, 20);
      displayChapters.forEach((chapter, index) => {
        displayChapterInfo(chapter, index + 1);
        console.log('');
      });

      // Step 3: Get detailed info for first 3 chapters
      console.log('\n' + '═'.repeat(80));
      console.log('DETAILED CHAPTER INFORMATION (First 3 Chapters)');
      console.log('═'.repeat(80));

      chaptersToDetail = formattedChapters.slice(0, 3);
    }

    // Get detailed information for selected chapters
    for (let i = 0; i < chaptersToDetail.length; i++) {
      const chapter = chaptersToDetail[i];

      console.log(`\n${'─'.repeat(80)}`);
      console.log(`📄 Getting details for Chapter ${chapter.chapter || 'N/A'}...`);
      console.log('─'.repeat(80));

      // Add delay to respect rate limits
      await sleep(250);

      try {
        const detailedChapter = await client.getChapterDetails(chapter.id);
        const detailedInfo = formatChapterInfo(detailedChapter);

        console.log(`\nChapter ID: ${detailedInfo.id}`);
        console.log(`Volume: ${detailedInfo.volume}`);
        console.log(`Chapter: ${detailedInfo.chapter}`);
        console.log(`Title: ${detailedInfo.title}`);
        console.log(`Pages: ${detailedInfo.pages}`);
        console.log(`Language: ${detailedInfo.language}`);
        console.log(`Scanlation Group: ${detailedInfo.scanlationGroup}`);
        console.log(`Uploader: ${detailedInfo.uploader}`);
        console.log(`Published: ${detailedInfo.publishAt}`);

        // Optional: Show how to get image URLs (commented out to avoid rate limiting)
        console.log('\n💡 To download images, use:');
        console.log(`   const imageData = await client.getChapterImages('${chapter.id}');`);
        console.log(`   const imageUrls = client.buildImageUrls(imageData, 'data');`);

      } catch (error) {
        console.error(`❌ Failed to get details for chapter ${chapter.chapter}: ${error.message}`);
      }
    }

    // Download images for the chapter
    console.log('\n' + '═'.repeat(80));
    console.log('IMAGE DOWNLOAD');
    console.log('═'.repeat(80));

    try {
      if (targetChapterNumber) {
        // Download the specific chapter that was found
        const chapterToDownload = chaptersToDetail[0];
        await downloadChapterImages(client, chapterToDownload.id, chapterToDownload, selectedManga.title);
      } else {
        // Download the latest chapter (first in the list)
        const latestChapter = formattedChapters[0];
        console.log(`Downloading latest chapter: ${latestChapter.chapter}`);
        await downloadChapterImages(client, latestChapter.id, latestChapter, selectedManga.title);
      }
    } catch (error) {
      console.error(`\n❌ Download failed: ${error.message}`);
    }

    // Summary
    console.log('\n' + '═'.repeat(80));
    console.log('SUMMARY');
    console.log('═'.repeat(80));
    console.log(`Manga: ${selectedManga.title}`);
    console.log(`Total Chapters Found: ${chapters.length}`);
    console.log(`Detailed Chapters Shown: ${chaptersToDetail.length}`);
    if (targetChapterNumber) {
      console.log(`Target Chapter: ${targetChapterNumber}`);
    }
    console.log('\n✅ Demo completed successfully!');
    console.log('\n💡 API Endpoints used:');
    console.log('   - GET /manga?title={query}');
    console.log('   - GET /manga/{mangaId}/feed');
    console.log('   - GET /chapter/{chapterId}');

  } catch (error) {
    console.error('\n❌ An error occurred:', error.message);
    if (error.response?.status === 429) {
      console.error('⚠️  Rate limit exceeded. Please wait and try again.');
    }
    process.exit(1);
  }
}

// Run the main function
main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
