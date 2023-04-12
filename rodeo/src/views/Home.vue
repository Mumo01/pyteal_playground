<template>
  <div class="home">
    <div class="blog-card-wrap">
      <div class="container">
    <div class="blog-cards">
     <!-- <PropertyCard :post="post" v-for="(post, index) in samplePropertyCards" :key="index" /> -->
     <ProjectCard :post="post" v-for="(post, index) in sampleProjectCard" :key="index" /> 
     <MessagesCard :post="post" v-for="(post, index) in sampleMessagesCard" :key="index" /> 

  </div>
    </div>
    </div>
  </div>
</template>

<script>
import PropertyCard from '../components/PropertyCard';
import ProjectCard from '../components/ProjectCard';
import MessagesCard from '../components/MessagesCard';

export default {
  name: "Home",
  components: {
    PropertyCard,
    ProjectCard, 
    MessagesCard
  },
  data() {
    return {
      samplePropertyCards: [
        { blogTitle: "Blog Card #1", blogCoverPhoto: "stock-1", blogDate: "May 1, 2023"},
        { blogTitle: "Blog Card #2", blogCoverPhoto: "stock-2", blogDate: "May 1, 2023"},
        { blogTitle: "Blog Card #3", blogCoverPhoto: "stock-3", blogDate: "May 1, 2023"},
        { blogTitle: "Blog Card #4", blogCoverPhoto: "stock-4", blogDate: "May 1, 2023"},
        { blogTitle: "Blog Card #4", blogCoverPhoto: "stock-4", blogDate: "May 1, 2023"},
        { blogTitle: "Blog Card #4", blogCoverPhoto: "stock-4", blogDate: "May 1, 2023"},
      ],
      sampleProjectCard: [
      { projectTitle: "Projects", blogCoverPhoto: "messages", projectInfo: "Join Project"},
      ],
      sampleMessagesCard: [
      { messagesTitle: "Messages", blogCoverPhoto: "messages", messagesInfo: "Send Messages"},
      ]
    }
  }
};
</script>
