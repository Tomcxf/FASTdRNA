library(ggplot2)
library(hrbrthemes)
library(viridis)
library(cowplot)
library(showtext)
font_add('Arial','/Library/Fonts/Arial.ttf') 
showtext_auto() 

percontig <- read.csv(snakemake@input[[1]],sep = "\t",header = F)
contigsummary <- aggregate(percontig$V9,by=list(type=percontig$V2),mean)
contigsummary$y <- c("plus")


p1 <- ggplot(contigsummary) +
  geom_violin(mapping = aes(x=contigsummary$y,y=contigsummary$x),width=0.6,fill="#5A005A") + 
  geom_boxplot(mapping=aes(x=contigsummary$y,y=contigsummary$x), color="grey",width=0.1, alpha=0.2) +
  scale_fill_viridis(discrete = TRUE) +
  theme_ipsum() +
  theme(
    legend.position="none",
    plot.title = element_text(size=16,hjust = 0.5),
    axis.text.y = element_text(size = 10, family = "myFont", vjust = 0.5, hjust = 0.5),
    axis.title.y = element_text(size=13, face="plain" , vjust = 10.2, hjust = 0.5),
    axis.title.x = element_text(size=13, face="plain" ,  hjust = 0.5),
    panel.border = element_blank(),
    axis.line = element_line(size=1, colour = "black")
  ) +
  ggtitle("Poly(A) Length of Reads") +
  theme(axis.text.x = element_blank()) +
  xlab("Reads") +
  ylab("Poly(A) Length (nt)")



p2 <- ggplot(percontig) + 
  geom_violin(mapping = aes(x=percontig$V10,y=percontig$V9),width=0.6,fill="#316397")+
  geom_boxplot(mapping=aes(x=percontig$V10,y=percontig$V9), color="grey",width=0.1, alpha=0.2) +
  scale_fill_viridis(discrete = TRUE) +
  theme_ipsum() +
  theme(
    legend.position="none",
    plot.title = element_text(size=16,hjust = 0.5),
    axis.text.y = element_text(size = 10, family = "myFont", vjust = 0.5, hjust = 0.5),
    axis.title.y = element_text(size=13, face="plain" , vjust = 10.2, hjust = 0.5),
    axis.title.x = element_text(size=13, face="plain" , hjust = 0.5),
    panel.border = element_blank(),
    axis.line = element_line(size=1, colour = "black")
  ) +
  ggtitle("Poly(A) Length of Contigs") +
  theme(axis.text.x = element_blank()) +
  xlab("Contigs") +
  ylab("Poly(A) Length (nt)")

cowplot::plot_grid(p1, p2, ncol = 2,labels = LETTERS[1:2])

ggsave(snakemake@output[[1]],width = 20, height = 20)

